import { createClient } from "npm:@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Vary": "Origin",
};

const allowedOrigins = new Set(
  (Deno.env.get("SITE_ALLOWED_ORIGINS") ?? "")
    .split(",")
    .map(origin => origin.trim().replace(/\/$/, ""))
    .filter(Boolean),
);

const JSON_BODY_LIMIT_BYTES = 16 * 1024;
const RATE_LIMITS: Record<string, { limit: number; windowSeconds: number }> = {
  list: { limit: 600, windowSeconds: 900 },
  "track-view": { limit: 300, windowSeconds: 3600 },
  "admin-login": { limit: 10, windowSeconds: 900 },
  submit: { limit: 5, windowSeconds: 3600 },
  "suggest-edit": { limit: 10, windowSeconds: 3600 },
  "admin-dashboard": { limit: 120, windowSeconds: 900 },
  review: { limit: 60, windowSeconds: 900 },
  delete: { limit: 30, windowSeconds: 900 },
  update: { limit: 60, windowSeconds: 900 },
  "review-suggestion": { limit: 60, windowSeconds: 900 },
};

function json(body: unknown, status = 200, extraHeaders: Record<string, string> = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json; charset=utf-8", ...extraHeaders },
  });
}

function clean(value: unknown, maxLength: number) {
  return typeof value === "string" ? value.trim().slice(0, maxLength) : "";
}

async function readJson(request: Request): Promise<Record<string, unknown>> {
  const reader = request.body?.getReader();
  if (!reader) throw new Error("Missing request body");
  const chunks: Uint8Array[] = [];
  let totalBytes = 0;
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    totalBytes += value.byteLength;
    if (totalBytes > JSON_BODY_LIMIT_BYTES) {
      await reader.cancel();
      throw new Error("Request body is too large");
    }
    chunks.push(value);
  }
  const bytes = new Uint8Array(totalBytes);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }
  const parsed: unknown = JSON.parse(new TextDecoder().decode(bytes));
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("Invalid JSON object");
  return parsed as Record<string, unknown>;
}

const projectUrl = Deno.env.get("SUPABASE_URL");
const secretKeys = JSON.parse(Deno.env.get("SUPABASE_SECRET_KEYS") ?? "{}");
const serviceKey = secretKeys.default ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

if (!projectUrl || !serviceKey) throw new Error("Supabase server credentials are unavailable.");

const db = createClient(projectUrl, serviceKey, {
  auth: { autoRefreshToken: false, persistSession: false },
});

const hmacKeyPromise = crypto.subtle.importKey(
  "raw",
  new TextEncoder().encode(serviceKey),
  { name: "HMAC", hash: "SHA-256" },
  false,
  ["sign"],
);

function clientIp(request: Request): string {
  const forwarded = request.headers.get("cf-connecting-ip")
    ?? request.headers.get("x-real-ip")
    ?? request.headers.get("x-forwarded-for")?.split(",")[0];
  return forwarded?.trim().slice(0, 100) ?? "";
}

async function rateLimitResponse(scope: string, identity: string, limit: number, windowSeconds: number): Promise<Response | null> {
  const key = await hmacKeyPromise;
  const signature = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${scope}:${identity}`));
  const bucketKey = Array.from(new Uint8Array(signature), byte => byte.toString(16).padStart(2, "0")).join("");
  const { data, error } = await db.rpc("consume_directory_rate_limit", {
    p_bucket_key: bucketKey,
    p_limit: limit,
    p_window_seconds: windowSeconds,
  });
  if (error || !data?.[0]) {
    console.error("Directory rate limiter is unavailable", error);
    return json({ error: "This service is temporarily unavailable. Please try again shortly." }, 503);
  }
  if (!data[0].allowed) {
    const retryAfter = Number(data[0].retry_after_seconds) || windowSeconds;
    return json(
      { error: "Too many requests. Please try again later." },
      429,
      { "Retry-After": String(retryAfter) },
    );
  }
  return null;
}

async function requireAdmin(request: Request) {
  const accessToken = request.headers.get("Authorization")?.replace(/^Bearer\s+/i, "");
  if (!accessToken || accessToken === serviceKey) return null;

  const { data: authData, error: authError } = await db.auth.getUser(accessToken);
  if (authError || !authData.user) return null;

  const { data: admin, error } = await db
    .from("directory_admins")
    .select("user_id")
    .eq("user_id", authData.user.id)
    .maybeSingle();
  if (error || !admin) return null;
  return authData.user;
}

async function handleRequest(request: Request): Promise<Response> {
  if (request.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });

  const action = new URL(request.url).searchParams.get("action");
  const rateLimit = action ? RATE_LIMITS[action] : undefined;
  if (rateLimit) {
    const ip = clientIp(request);
    if (!ip) return json({ error: "Could not verify request source. Please try again shortly." }, 503);
    const blocked = await rateLimitResponse(`ip:${action}`, ip, rateLimit.limit, rateLimit.windowSeconds);
    if (blocked) return blocked;
  }
  if (request.method === "POST" && Number(request.headers.get("content-length") ?? 0) > JSON_BODY_LIMIT_BYTES) {
    return json({ error: "Request body is too large." }, 413);
  }

  if (request.method === "GET" && action === "list") {
    const { data, error } = await db
      .from("churches")
      .select("id,name,pastor,country,state,city,address,zip,email,phone,fax,website,description,status,created_at")
      .eq("status", "approved")
      .order("country")
      .order("city");
    if (error) return json({ error: "Could not load the directory." }, 500);
    return json({ churches: data ?? [] });
  }

  if (request.method === "POST" && action === "track-view") {
    const { error } = await db.rpc("increment_directory_daily_views");
    if (error) {
      console.error("Could not record directory view", error);
      return json({ error: "Could not record this view." }, 500);
    }
    return json({ ok: true }, 201);
  }

  if (request.method === "POST" && action === "admin-login") {
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Invalid sign-in details." }, 400); }
    const username = clean(input.username, 64).toLowerCase();
    const password = typeof input.password === "string" ? input.password : "";
    if (!/^[a-z0-9._-]{3,64}$/.test(username) || !password || password.length > 256) {
      return json({ error: "Invalid username or password." }, 401);
    }
    const usernameBlocked = await rateLimitResponse("username:admin-login", username, 5, 900);
    if (usernameBlocked) return usernameBlocked;

    const { data: admin, error: adminError } = await db
      .from("directory_admins")
      .select("user_id")
      .eq("username", username)
      .maybeSingle();
    if (adminError || !admin) return json({ error: "Invalid username or password." }, 401);

    const { data: account, error: accountError } = await db.auth.admin.getUserById(admin.user_id);
    if (accountError || !account.user?.email) return json({ error: "Invalid username or password." }, 401);

    const publishableKey = request.headers.get("apikey");
    if (!publishableKey) return json({ error: "Sign-in is unavailable." }, 400);
    const authClient = createClient(projectUrl!, publishableKey, {
      auth: { autoRefreshToken: false, persistSession: false },
    });
    const { data: signedIn, error: signInError } = await authClient.auth.signInWithPassword({
      email: account.user.email,
      password,
    });
    if (signInError || !signedIn.session || signedIn.user.id !== admin.user_id) {
      return json({ error: "Invalid username or password." }, 401);
    }

    return json({ access_token: signedIn.session.access_token });
  }

  if (request.method === "POST" && action === "submit") {
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Please submit valid church details." }, 400); }
    if (clean(input.company_website, 200)) return json({ ok: true });

    const church = {
      name: clean(input.name, 160), pastor: clean(input.pastor, 160), country: clean(input.country, 100),
      state: clean(input.state, 100), city: clean(input.city, 100), address: clean(input.address, 300),
      zip: clean(input.zip, 40), email: clean(input.email, 254), phone: clean(input.phone, 50),
      fax: clean(input.fax, 50), website: clean(input.website, 300), description: clean(input.description, 1200),
      status: "pending",
    };
    if (!church.name || !church.country || !church.city) {
      return json({ error: "Church name, country, and city are required." }, 400);
    }
    const emailParts = church.email.split("@");
    if (church.email && (emailParts.length !== 2 || !emailParts[0] || !emailParts[1].includes(".") || church.email.includes(" "))) {
      return json({ error: "Please provide a valid email address." }, 400);
    }
    const { error } = await db.from("churches").insert(church);
    if (error) return json({ error: "Your request could not be saved. Please try again later." }, 500);
    return json({ ok: true }, 201);
  }

  if (request.method === "POST" && action === "suggest-edit") {
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Please submit valid details." }, 400); }
    if (clean(input.company_website, 200)) return json({ ok: true });
    const churchId = clean(input.church_id, 200);
    const changes = {
      name: clean(input.name, 160), pastor: clean(input.pastor, 160), country: clean(input.country, 100),
      state: clean(input.state, 100), city: clean(input.city, 100), address: clean(input.address, 300),
      zip: clean(input.zip, 40), email: clean(input.email, 254), phone: clean(input.phone, 50),
      fax: clean(input.fax, 50), website: clean(input.website, 300), description: clean(input.description, 1200),
    };
    if (!churchId || !changes.name || !changes.country || !changes.city) {
      return json({ error: "Church name, country, and city are required." }, 400);
    }
    const emailParts = changes.email.split("@");
    if (changes.email && (emailParts.length !== 2 || !emailParts[0] || !emailParts[1].includes(".") || changes.email.includes(" "))) {
      return json({ error: "Please provide a valid email address." }, 400);
    }
    const { data: church, error: churchError } = await db.from("churches").select("id")
      .eq("id", churchId).eq("status", "approved").maybeSingle();
    if (churchError) return json({ error: "Could not check this church listing." }, 500);
    if (!church) return json({ error: "This church is not available for edit suggestions." }, 404);
    const { error } = await db.from("church_edit_suggestions").insert({ church_id: churchId, changes });
    if (error) {
      console.error("Could not save church edit suggestion", error);
      return json({ error: "Your suggested changes could not be saved." }, 500);
    }
    return json({ ok: true }, 201);
  }

  if (action === "admin-dashboard" && request.method === "GET") {
    const admin = await requireAdmin(request);
    if (!admin) return json({ error: "Admin access is required." }, 403);

    const requestedDays = Number(new URL(request.url).searchParams.get("days"));
    const periodDays = [7, 30, 90, 365].includes(requestedDays) ? requestedDays : 30;
    const since = new Date();
    since.setUTCDate(since.getUTCDate() - (periodDays * 2 - 1));
    const startDate = since.toISOString().slice(0, 10);
    const endDate = new Date().toISOString().slice(0, 10);
    const [pendingResult, approvedResult, viewsResult, churchesResult, suggestionsResult] = await Promise.all([
      db.from("churches").select("id,name,pastor,country,state,city,address,zip,email,phone,fax,website,description,status,created_at")
        .eq("status", "pending").order("created_at", { ascending: true }),
      db.from("churches").select("id", { count: "exact", head: true }).eq("status", "approved"),
      db.from("directory_daily_views").select("view_date,views").gte("view_date", startDate).lte("view_date", endDate).order("view_date"),
      db.from("churches").select("id,name,pastor,country,state,city,address,zip,email,phone,fax,website,description,status,created_at")
        .order("country").order("city").order("name"),
      db.from("church_edit_suggestions").select("id,church_id,changes,status,created_at")
        .eq("status", "pending").order("created_at", { ascending: true }),
    ]);
    if (pendingResult.error || approvedResult.error || viewsResult.error || churchesResult.error || suggestionsResult.error) {
      console.error("Admin dashboard query failed", pendingResult.error, approvedResult.error, viewsResult.error, churchesResult.error, suggestionsResult.error);
      return json({ error: "Could not load admin information." }, 500);
    }
    return json({
      admin: { email: admin.email },
      pending: pendingResult.data ?? [],
      suggestions: suggestionsResult.data ?? [],
      churches: churchesResult.data ?? [],
      approvedCount: approvedResult.count ?? 0,
      dailyViews: viewsResult.data ?? [],
      analyticsRangeDays: periodDays,
    });
  }

  if (action === "review" && request.method === "POST") {
    if (!await requireAdmin(request)) return json({ error: "Admin access is required." }, 403);
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Invalid review request." }, 400); }
    const id = clean(input.id, 200);
    const status = clean(input.status, 20);
    if (!id || !["approved", "rejected"].includes(status)) return json({ error: "Invalid review decision." }, 400);
    const { data, error } = await db.from("churches").update({ status }).eq("id", id).eq("status", "pending").select("id").maybeSingle();
    if (error) return json({ error: "Could not update this church." }, 500);
    if (!data) return json({ error: "This pending church was not found." }, 404);
    return json({ ok: true });
  }

  if (action === "delete" && request.method === "POST") {
    if (!await requireAdmin(request)) return json({ error: "Admin access is required." }, 403);
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Invalid delete request." }, 400); }
    const id = clean(input.id, 200);
    if (!id) return json({ error: "Church ID is required." }, 400);
    const { data, error } = await db.from("churches").delete().eq("id", id).select("id").maybeSingle();
    if (error) return json({ error: "Could not delete this church." }, 500);
    if (!data) return json({ error: "Church was not found." }, 404);
    return json({ ok: true });
  }

  if (action === "update" && request.method === "POST") {
    if (!await requireAdmin(request)) return json({ error: "Admin access is required." }, 403);
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Invalid update request." }, 400); }
    const id = clean(input.id, 200);
    const church = {
      name: clean(input.name, 160), pastor: clean(input.pastor, 160), country: clean(input.country, 100),
      state: clean(input.state, 100), city: clean(input.city, 100), address: clean(input.address, 300),
      zip: clean(input.zip, 40), email: clean(input.email, 254), phone: clean(input.phone, 50),
      fax: clean(input.fax, 50), website: clean(input.website, 300), description: clean(input.description, 1200),
    };
    if (!id || !church.name || !church.country || !church.city) {
      return json({ error: "Church name, country, and city are required." }, 400);
    }
    const emailParts = church.email.split("@");
    if (church.email && (emailParts.length !== 2 || !emailParts[0] || !emailParts[1].includes(".") || church.email.includes(" "))) {
      return json({ error: "Please provide a valid email address." }, 400);
    }
    const { data, error } = await db.from("churches").update(church).eq("id", id).select("id").maybeSingle();
    if (error) return json({ error: "Could not update this church." }, 500);
    if (!data) return json({ error: "Church was not found." }, 404);
    return json({ ok: true });
  }

  if (action === "review-suggestion" && request.method === "POST") {
    if (!await requireAdmin(request)) return json({ error: "Admin access is required." }, 403);
    let input: Record<string, unknown>;
    try { input = await readJson(request); } catch { return json({ error: "Invalid suggestion review." }, 400); }
    const suggestionId = clean(input.id, 80);
    const decision = clean(input.decision, 20);
    if (!suggestionId || !["approved", "rejected"].includes(decision)) {
      return json({ error: "Invalid suggestion review." }, 400);
    }
    const { data, error } = await db.rpc("review_church_edit_suggestion", {
      p_suggestion_id: suggestionId,
      p_decision: decision,
    });
    if (error) {
      console.error("Could not review church edit suggestion", error);
      return json({ error: "Could not review this suggestion." }, 500);
    }
    if (!data) return json({ error: "This pending suggestion was not found." }, 404);
    return json({ ok: true });
  }

  return json({ error: "Not found." }, 404);
}

Deno.serve(async (request) => {
  const origin = request.headers.get("origin")?.replace(/\/$/, "");
  if (origin && allowedOrigins.size > 0 && !allowedOrigins.has(origin)) {
    return new Response(JSON.stringify({ error: "Origin is not allowed." }), {
      status: 403,
      headers: { "Content-Type": "application/json; charset=utf-8", "Vary": "Origin" },
    });
  }

  const response = await handleRequest(request);
  if (origin) response.headers.set("Access-Control-Allow-Origin", allowedOrigins.size ? origin : "*");
  response.headers.set("Vary", "Origin");
  return response;
});
