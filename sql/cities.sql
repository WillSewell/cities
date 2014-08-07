CREATE TABLE cities
(
  local_name character(80),
  eng_name character(80),
  country character(80),
  agglom_population integer,
  city_id serial NOT NULL,
  CONSTRAINT pk_city_id PRIMARY KEY (city_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE cities
  OWNER TO postgres;
