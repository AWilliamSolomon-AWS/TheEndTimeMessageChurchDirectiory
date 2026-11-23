create table if not exists public.churches (
  id text primary key default gen_random_uuid()::text,
  name text not null,
  pastor text,
  country text not null,
  state text,
  city text not null,
  address text,
  zip text,
  email text,
  phone text,
  fax text,
  website text,
  description text,
  status text not null default 'pending' check (status in ('pending', 'approved', 'rejected')),
  created_at timestamptz not null default now()
);

create index if not exists churches_status_location_idx
  on public.churches (status, country, city);

alter table public.churches enable row level security;
revoke all on public.churches from anon, authenticated;

insert into public.churches
  (id, name, pastor, country, state, city, address, zip, email, phone, fax, website, description, status, created_at)
values
  ('pillar-of-fire', 'The Pillar of Fire Ministries', 'K. Andrew', 'India', 'Telangana', 'Hyderabad', '14-B, Gospel Lane', '500001', 'contact@pillaroffire.in', '+91 98765 43210', '', 'www.pillaroffire.in', 'An end-time message fellowship serving believers in Hyderabad.', 'approved', '2026-10-01T00:00:00Z'),
  ('ljc-tabernacle', 'Lord Jesus Christ Tabernacle', 'JohnPaul Nannepanga', 'India', 'Telangana', 'Warangal', 'Church Road, Hanamkonda', '506001', '', '+91 94404 12345', '', '', 'End-time Message Assembly in Warangal.', 'approved', '2026-10-02T00:00:00Z'),
  ('bible-believers', 'Bible Believers', 'Ivan Ockhuis', 'South Africa', 'Western Cape', 'Cape Town', '12 Vineyard Street', '8001', 'info@biblebelievers.co.za', '+27 21 555 0100', '+27 21 555 0101', 'www.biblebelievers.co.za', 'Serving message believers in Cape Town.', 'approved', '2026-10-03T00:00:00Z')
on conflict (id) do nothing;
