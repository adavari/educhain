alter table transaction
	add keyword uuid default '9cda113d-e236-47a1-9692-0cd87a6dc2f9'::uuid not null;

alter table transaction
	add constraint transaction_keyword_id_fk
		foreign key (keyword) references distribution
			on update cascade on delete cascade;

