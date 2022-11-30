create table channel_admin
(
	id uuid
		constraint channel_admin_pk
			primary key,
	username varchar(255) not null,
	password varchar(255) not null,
	payment_account varchar(255),
	payment_bank_name varchar(255),
	credit_card_number varchar(16),
	credit_card_name varchar(255),
	channel_name varchar(255) not null,
	channel_id varchar(255) not null,
	status int default 0,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

create unique index channel_admin_channel_id_uindex
	on channel_admin (channel_id);

create unique index channel_admin_username_uindex
	on channel_admin (username);

alter table users
	add keyword uuid;

alter table channel_admin
	add name varchar(255);


alter table channel_admin drop column channel_name;

drop index channel_admin_channel_id_uindex;

alter table channel_admin drop column channel_id;

create unique index channel_admin_channel_id_uindex
	on channel_admin (channel_id);

create table distribution
(
	id uuid
		constraint distribution_pk
			primary key,
	name varchar(255) not null,
	platform varchar(255) not null,
	channel_id varchar(255) not null,
	channel_owner uuid not null
		constraint distribution_owner_channel_admin_fk
			references channel_admin
				on update cascade on delete cascade,
	status int default 0,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

create unique index distribution_platform_channel_id_index
	on distribution (channel_id, platform);


alter table users
	add constraint users_keyword_distribution_fk
		foreign key (keyword) references distribution
			on update cascade on delete cascade;

insert into channel_admin (id, username, password, payment_account, payment_bank_name, credit_card_number, credit_card_name, name)
values (uuid_generate_v5('7aa1c5f9-5062-47a3-a166-be7ededfad66', 'admin'), 'admin', '09c6abf7c3ee5a4f00a7817fd04ff013cab5e391', '12345', 'JIB', '1234123412341234', 'mellat', 'akhaee');

insert into distribution (id, name, platform, channel_id, channel_owner, status)
values ('9cda113d-e236-47a1-9692-0cd87a6dc2f9', 'main', 'site', 'www.edu-chains.com', '1f468aa9-ee99-50d1-9fa2-366df515c448', 1);

alter table users alter column keyword set default '9cda113d-e236-47a1-9692-0cd87a6dc2f9';

alter table distribution alter column id set default uuid_generate_v4();

