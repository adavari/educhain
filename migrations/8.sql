create table balance
(
	id uuid default uuid_generate_v4()
		constraint balance_pk
			primary key,
	channel_admin_id uuid not null
		constraint balance_channel_admin_id_fk
			references channel_admin
				on update cascade on delete cascade,
	amount bigint not null,
	created_at timestamp default now(),
	updated_at timestamp default now()
);

