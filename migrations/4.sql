create table category
(
	id uuid default uuid_generate_v4(),
	name varchar(255) not null
);

create unique index category_id_uindex
	on category (id);

alter table category
	add constraint category_pk
		primary key (id);


create function random_bytea(p_length in integer) returns bytea language plpgsql as $$
declare
  o bytea := '';
begin
  for i in 1..p_length loop
    o := o||decode(lpad(to_hex(width_bucket(random(), 0, 1, 256)-1),2,'0'), 'hex');
  end loop;
  return o;
end;$$;

alter table course
	add aes_key bytea default random_bytea(16);

alter table course
	add aes_iv bytea default random_bytea(16);
