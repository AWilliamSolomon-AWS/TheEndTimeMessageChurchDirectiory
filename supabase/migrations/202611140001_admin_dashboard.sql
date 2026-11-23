-- Private administrator allowlist. Add only trusted Supabase Auth user IDs here.
create table if not exists public.directory_admins (
  user_id uuid primary key references auth.users (id) on delete cascade,
  username text not null unique check (username = lower(username) and username ~ '^[a-z0-9._-]{3,64}$'),
  created_at timestamptz not null default now()
);
alter table public.directory_admins enable row level security;
revoke all on public.directory_admins from anon, authenticated;
grant select on public.directory_admins to service_role;

-- Aggregate daily page views only; no visitor names, IP addresses, or contact data.
create table if not exists public.directory_daily_views (
  view_date date primary key,
  views bigint not null default 0 check (views >= 0)
);
alter table public.directory_daily_views enable row level security;
revoke all on public.directory_daily_views from anon, authenticated;
grant select, insert, update on public.directory_daily_views to service_role;

create or replace function public.increment_directory_daily_views()
returns void
language sql
security definer
set search_path = ''
as $$
  insert into public.directory_daily_views (view_date, views)
  values (current_date, 1)
  on conflict (view_date)
  do update set views = public.directory_daily_views.views + 1;
$$;
revoke all on function public.increment_directory_daily_views() from public, anon, authenticated;
grant execute on function public.increment_directory_daily_views() to service_role;

create table if not exists public.church_edit_suggestions (
  id uuid primary key default gen_random_uuid(),
  church_id text not null references public.churches (id) on delete cascade,
  changes jsonb not null check (jsonb_typeof(changes) = 'object'),
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at timestamptz not null default now()
);
create index if not exists church_edit_suggestions_status_created_idx
  on public.church_edit_suggestions (status, created_at);
alter table public.church_edit_suggestions enable row level security;
revoke all on public.church_edit_suggestions from anon, authenticated;
grant select, insert, update, delete on public.church_edit_suggestions to service_role;

create or replace function public.review_church_edit_suggestion(p_suggestion_id uuid, p_decision text)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  suggestion public.church_edit_suggestions%rowtype;
begin
  if p_decision not in ('approved', 'rejected') then
    raise exception 'Invalid review decision';
  end if;

  select * into suggestion
  from public.church_edit_suggestions
  where id = p_suggestion_id and status = 'pending'
  for update;
  if not found then return false; end if;

  if p_decision = 'approved' then
    update public.churches
    set name = coalesce(suggestion.changes ->> 'name', name),
        pastor = coalesce(suggestion.changes ->> 'pastor', pastor),
        country = coalesce(suggestion.changes ->> 'country', country),
        state = coalesce(suggestion.changes ->> 'state', state),
        city = coalesce(suggestion.changes ->> 'city', city),
        address = coalesce(suggestion.changes ->> 'address', address),
        zip = coalesce(suggestion.changes ->> 'zip', zip),
        email = coalesce(suggestion.changes ->> 'email', email),
        phone = coalesce(suggestion.changes ->> 'phone', phone),
        fax = coalesce(suggestion.changes ->> 'fax', fax),
        website = coalesce(suggestion.changes ->> 'website', website),
        description = coalesce(suggestion.changes ->> 'description', description)
    where id = suggestion.church_id;
    if not found then return false; end if;
  end if;

  update public.church_edit_suggestions
  set status = p_decision
  where id = p_suggestion_id;
  return true;
end;
$$;
revoke all on function public.review_church_edit_suggestion(uuid, text) from public, anon, authenticated;
grant execute on function public.review_church_edit_suggestion(uuid, text) to service_role;

grant select, insert, update, delete on public.churches to service_role;
