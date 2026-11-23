-- Additive import of the 48 "End Time Message" search results visible in the
-- Living Word Broadcast church directory on 2026-11-19.
-- Emails on the source site are rendered as protected images and are omitted.
-- This is idempotent: existing entries with the same name/country/city are kept.
with source_rows(name, pastor, country, city, address, phone, website, fax) as (
  values
    ('End Time Message', 'Pastor Roshan Masih', 'India', 'HOSHIARPUR', 'SHAM CHAURASI, HOSHIARPUR, PUNJAB, 144105', '+919463305712', 'http:// risingofthesun.org', ''),
    ('Calvary Tabernacle (End-Time Tamil Church)', 'Pastor A.Samuel', 'India', 'Chennai', '8/10 Kalaigner Street, Chennai, Tamil Nadu, 600087', '', 'http://calvarytabernacle.in and http;//calvarytabernaclemessage.in', ''),
    ('End Time Message Tabernacle', 'Paul Musulube', 'Uganda', 'Iganga', 'P.O. Box 668, Iganga, 256', '+256772563547', '', ''),
    ('The End Time Message Kampala Church', 'Office Assistant', 'Uganda', 'Kampala', 'P.O.Box 20089, Kampala', '+256-414-574300', '', ''),
    ('mbeya endtime mmessage church', 'Bro.Umoti Lusanjala', 'Tanzania', 'Mbeya', 'sistila nearby TBL Co.,iyunga, Mbeya, p.o.box 1216', '0715 999 866', '', ''),
    ('END TIME MESSAGE-HOSSANA TABERNACLE', 'Pastor Phillimon HARAWA', 'Malawi', 'MZUZU', 'P.O.Box221,NKHATA-BAY, MZUZU', '+265 88 123 9162, +265 99 1147 655', '', ''),
    ('CAPSTONE REVIVAL CENTRE, END TIME MESSAGE LOCAL CHRISTIAN FELLOWSHIP', 'BRO. ATAKWA BULLEY', 'Nigeria', 'CALABAR', 'MEKENGE LAYOUT, CALABAR, CROSS RIVER STATE, 540221', '+2348023515610', '', ''),
    ('Luve End Time Message Tabernacle', 'â��+268 7657 5842', 'Swaziland', 'Mbabane', 'P.O. Box 6664, Manzini Eswatini, Mbabane, Manzini, M200', '+268 76729595', '', ''),
    ('End Time Message Believers', '03424210762', 'Pakistan', 'Lahore', 'Asif Town No 2 Ferozpur Road Lahore, Lahore, Punjab', '03244531903', '', ''),
    ('End time Message believers Fellowship Pakistn', 'Pastor Jamil Younas', 'Pakistan', 'Rawalpindi', 'House #SN-853, Street #17-CMohalla Jinnah Town, Dhoke Kala Khan, Rawalpindi, Punjab', '0092335523770', '', ''),
    ('UBUNGO ENDTIME MESSAGE CHURCH', 'Bro.Shindano Shija', 'Tanzania', 'DAR ES SALAAM', 'UBUNGO, JUST CLOSE TO MABIBO HOSTEL , DAR ES SALAAM', '+255 732 201352.', 'http://endtimemessage.or.tz', ''),
    ('End time Message church', 'Pastor Babar Saleem', 'Pakistan', 'Islamabad', 'Essa naghri Islamabad , Islamabad, Pakistan', '00923120529175', 'http://', ''),
    ('End Time Message Fellowship', 'William Branham Frank', 'Vanuatu', 'Port Vila', 'PO Box 3552, Port Vila, Shefa Province, 678', '00678 7776606', 'http://--------------------------------------------------------', ''),
    ('ONLY BELIEVE TABERNACLE', 'BROTHER MALKEET SINGH', 'India', 'AMRITSAR', 'VPO MANAWALA KALAN, AMRITSAR, PUNJAB, 143115', '+91 9915082823', 'http://www.onlybelieve.in', ''),
    ('End Time Message Tabernacle', 'Timothy Ashong', 'Ghana', 'Accra', 'P.O. Box A457, Accra, Labadi', '', 'http://', ''),
    ('End Time Message Christian Tabernacle', 'Pastor Graciano T. Sacayan and Bro. Manny T. Sacayan', 'Philippines', 'Sagay City', 'Jison Subd.,, Sagay City, Negros Occidental, 6122', '', 'http://', ''),
    ('Jesus Voice Church (END TIME MESSAGE)', 'Pr.John Venkatesan and JOHNSON DAVIS', 'India', 'Cuddalore', 'cuddalore Old Town, Cuddalore, Tamil Nadu, 607003', '9976990115', '', ''),
    ('Faith Tabernacle', 'Pastor Jean- Pierre Luyeye', 'United States', 'Morrow', '2054 Rex Rd, Morrow, GA, 30260', '706 888 1674', 'http://Faithtabernacleendtimemessage.com', ''),
    ('End Time Message', 'Billy Steadward', 'United Kingdom', 'East Kilbride', '1 Walnut Lane, East Kilbride, South Lanarkshire , G75 9DY', '00441355457342', 'http://', ''),
    ('End Time Message Believers', 'Bro. Elton Desouza', 'Kuwait', 'Salmiya', 'Suleiman Asdani Str, Block 10, Salmiya', '+965 99857703', 'http://www.facebook.com/pages/Message-Church-Kuwait-House-of-Prayer/195882907109895', ''),
    ('End Time Message', 'Benon Caleb Arinaitwe', 'Uganda', 'Rukungiri', 'P.O. Box 101, Rukungiri', '', '', ''),
    ('The Endtime Message Church', 'Vincent Mukaga', 'Uganda', 'Bugiri', 'P.O. Box 73, Bugiri', '', '', ''),
    ('THE LORD JESUS CHRIST''S TABERNACLE-THE END-TIME MESSAGE', 'PASTOR.O.MARIAPPAN', 'India', 'Tiruchirappalli', '13/8,M.Seegampatty,pothapatty post, Elangakurichy-via , Tiruchirappalli , Tamilnadu , 621302', '+919159583422', 'http://www.thelordjesuschristtabernacle.org', '+919159583422'),
    ('THE LORD JESUS CHRIST''S TABERNACLE-THE END-TIME MESSAGE', 'PASTOR.MARIAPPAN', 'India', 'BANGALORE', 'FLOT#13,3/1.1ST''E''CROSS,NETHAJI CIRCLE,MATHIKERE, BANGALORE, KARNATAKA, 560054', '+919159583422', 'http://www.thelordjesuschristtabernacle.org', '+919159583422'),
    ('End Time Tabernacle', 'Pastor David Odoi', 'Ghana', 'LA, Accra', 'P.O. Box A 457, LA, Accra', '', '', ''),
    ('End Time Message Church', 'Pastor John Issac', 'India', 'Nungambakkam, chennai', 'Choolaimedu , Nungambakkam, chennai, Tamilnadu, 600 094', '09841559727', '', ''),
    ('Ngowane Endtime Message Church', 'Bro Phillip Mathunjwa', 'Swaziland', 'Pigg''s Peak', 'Ngowane Area, Pigg''s Peak, Hhohho', '+26876076601', '', ''),
    ('ENDTIME MESSAGE BELIEVERS', 'PASTOR BANNOR RANSFORD', 'Ghana', 'KUMASI', 'POST OFFICE BOX 24, JACHIE ASHANTI, KUMASI, ASHANTI REGION', '', 'http://', ''),
    ('Kafuga End Time Message', '+256787458385', 'Uganda', 'mbarara', 'rubuguri town council, mbarara, Kisoro', '+256787458385', '', ''),
    ('Luve Endtime Message Assembly', 'Bro Phillip Mathunjwa', 'Swaziland', 'Luve', 'Luve, Luve, Manzini', '+26876076601', '', ''),
    ('Bulanga End Time Message Church', 'Samson Lubogo', 'Uganda', 'Iganga', 'P.O. Box 312, Iganga', '', '', ''),
    ('End Time Message Tabernacle', 'Harold Hildebrandt', 'Canada', 'Edmonton', '9200-156 Street, Edmonton, Alberta, T5R 1Z1', '(780)489-1344', 'http://www.inthedaysofthevoice.com', ''),
    ('End Time Message Believers', 'Samuel Ngumbao', 'Kenya', 'Mombasa', 'P.O. Box 97896, Mombasa, Coast, 00254', '+254-736-190-393', '', ''),
    ('Voice of God Tabernacle', 'Ps. Peter Yakanu', 'Ghana', 'New Tafo Akim', 'End Time Message Tabernacle, P.O, Box 117, New Tafo Akim, New Tafo Akim, Eastern Region, 00233', '0547178662', '', ''),
    ('Spoken Word Christian Assembly', 'Ronnie Millevo', 'Philippines', 'Quezon City', '58 Sammar1 St, Old Balara,, Quezon City, Old Balara, 1119', '(632) 931-8796', 'http://endtimemessage.info', ''),
    ('BUKATUBE END TIME MESSAGE MINISTRY', 'Pastor Samuel Taganhye Wakato', 'Select Country', 'BUKATUBE TOWNSHIP', 'BuKatube /MAYUGE -, BUKATUBE TOWNSHIP, Eastern ð��ºð��¬Uganda, +256', '+256 758 042 019', '', ''),
    ('End Time Message Believers Assemblies Pakistan', '03224480832', 'Pakistan', 'Lahore', '4A Ahmed Street Bakar Colony Kotlakhpat, Lahore, Punjab', '9292401686', '', ''),
    ('The Lord Jesus Christ''s Tabernacle', 'Pastor O Mariappan', 'India', 'Tiruchirappalli', '13/8,M. Seegampatty, Mohovanoor post, Elangakurichy-via,, Tiruchirappalli , Tamil Nadu, 621302', '+919159583422', '', ''),
    ('End Time Message Believers Assembly', '042-35918441', 'Pakistan', 'Lahore', '4-A, Ahmed Street, Bahar Colony,Kot Lakhpat , Lahore, Punjab, 54770', '', 'http://Wwww.urdubride.com', ''),
    ('Kafuga End Time Message Church', 'Donati Bangangyira', 'Uganda', 'Kampala', 'Rubuguri, Kisoro Uganda, Kampala, Western Uganda(Kigezi), 7575', '+256770868899', 'http://branham.org', '+256784941914'),
    ('Little Bethlehem Church', 'Dean Gilchrist', 'New Zealand', 'Wanganui', '60 Kaikokopu Road, Wanganui, Manawatu, 4500', '', 'http://end-time-message.org', ''),
    ('End Time Message Believers Church -Sagana', 'Andrew Sikuku', 'Kenya', 'Nairobi', 'P.O Box 25002, Nairobi, SAGANA TOWN-KIRINYAGA COUNTY , 00100', '+254713405414', '', ''),
    ('End time message', '0400456', 'Australia', 'Brisbane', 'Brisbane, Brisbane , Qld, Brisbane', '0468522964', 'http://', ''),
    ('End Time Message Church', 'Hugh Jass', 'Vanuatu', 'Port Vila', 'P.O. Box 9541, Port Vila, Shef Province', '', '', ''),
    ('Lepanto Endtime Message Church', 'Bro. Daniel A. Baroy', 'Philippines', 'Mankayan', 'Lepanto, Mankayan, Benguet, 2609', '09202661352', '', ''),
    ('End Time Message Believers Ministry Pakistan', '0092 3458277705', 'Pakistan', 'Islamabad', 'Iqbal Town Islamabad, Islamabad, Capital , 44310', '0092 3458277705', 'http://https://thewordrevealed.info/', ''),
    ('Kabaale End Time Message Fellowship', 'India Joseph', 'Uganda', 'Hoima', 'P.O. Box 257, Hoima', '', '', ''),
    ('End Time Message Tabernacle', 'Faustin Lukumuena', 'United States', 'Denver', '14650 Chambers Rd, Denver, CO, 80601', '720-351-1127', 'http://etmtabernacle.org/', '')
), imported as (
  select
    'lwb-' || substr(md5(lower(name || '|' || country || '|' || city)), 1, 24) as id,
    name, nullif(pastor, '') as pastor, country, ''::text as state, city, nullif(address, '') as address,
    ''::text as zip, ''::text as email, nullif(phone, '') as phone, nullif(fax, '') as fax,
    nullif(website, '') as website,
    'Imported from the Living Word Broadcast Church Directory search results (Nov 2026). Source listings may be outdated; please confirm contact details.' as description,
    'approved'::text as status
  from source_rows
)
insert into public.churches
  (id, name, pastor, country, state, city, address, zip, email, phone, fax, website, description, status)
select i.id, i.name, i.pastor, i.country, i.state, i.city, i.address, i.zip, i.email, i.phone, i.fax, i.website, i.description, i.status
from imported i
where not exists (
  select 1 from public.churches c
  where lower(trim(c.name)) = lower(trim(i.name))
    and lower(trim(c.country)) = lower(trim(i.country))
    and lower(trim(c.city)) = lower(trim(i.city))
);
