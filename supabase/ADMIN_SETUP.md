# Admin dashboard setup

The website keeps the public directory open. Admin pages and moderation actions are protected by Supabase Auth plus the private `public.directory_admins` allowlist. Do not put an admin password or a Supabase service key in website files.

## Supabase setup

1. In Supabase SQL Editor, run `migrations/202611140001_admin_dashboard.sql`.
2. Run `migrations/202611230001_directory_rate_limits.sql` before deploying the updated function. The function fails closed if the rate-limit database function is missing.
3. To restrict cross-origin browser access, set the Edge Function secret `SITE_ALLOWED_ORIGINS` to the exact website origins, comma-separated (for example, `https://your-domain.example,https://www.your-domain.example`). Add any production custom domain and the exact preview origin you use. Do not include page paths or trailing slashes. If omitted, the public endpoints keep wildcard CORS for compatibility; this is not an access-control boundary.
4. In Edge Functions, open `church-directory`, replace its `index.ts` with `functions/church-directory/index.ts`, and deploy the update.
5. In Authentication → Users, create the administrator's email/password account. Do not enable public sign-up for this purpose.
6. Copy the administrator's user ID from Authentication → Users and add only that user to the allowlist with the username they will enter on the website:

```sql
insert into public.directory_admins (user_id, username)
values ('PASTE-AUTH-USER-UUID-HERE', lower('CHOOSE-ADMIN-USERNAME'))
on conflict (user_id) do nothing;
```

7. Publish the updated site files, including `admin-login.html`.

Only accounts in `directory_admins` can read pending submissions and edit suggestions, directly edit any listing, approve/reject submissions and suggestions, delete listings, or view daily directory counters. Public visitors can suggest changes to approved listings; suggested changes do not appear until an administrator approves them. The login page resolves the chosen username to its allowlisted Supabase Auth user and keeps the short-lived access token in memory; it is not saved in browser storage. Daily counts are aggregate counts only. Rate-limit bucket identifiers are HMACs made with the server-only Supabase service key; raw IP addresses and usernames are not stored.

The Edge Function applies per-IP limits: directory list 600 per 15 minutes; view tracking 300 per hour; admin sign-in 10 per 15 minutes (plus 5 per username per 15 minutes); church submissions 5 per hour; edit suggestions 10 per hour; dashboard reads 120 per 15 minutes; and admin moderation/edit actions 30–60 per 15 minutes. Requests over 16 KiB are rejected. A rate-limit database error returns `503` rather than allowing unbounded writes. The Edge Function URL and publishable key remain visible to browsers by design; this does not grant database access. RLS and server-side admin checks protect private data and actions. The origin allowlist reduces cross-origin browser calls, but it is not a substitute for authentication because non-browser clients can call public endpoints directly.
