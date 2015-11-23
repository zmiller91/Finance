create database TradingApi;
use TradingApi;

create table dimension_categories(
    dim_cat_id int not null auto_increment,
    dim_cat varchar(256) not null,
    primary key (dim_cat_id)
);

create table dimensions(
    dim_id int not null auto_increment,
    dim_name varchar(256) not null,
    dim_value varchar(256) not null,
    dim_cat_id int not null,
    primary key (dim_id),
    foreign key (dim_cat_id) references dimension_categories(dim_cat_id),
    unique (dim_name),
    unique (dim_value)
);

create table s_test_daily_data(
    date date not null,
    dim_name varchar(256) not null,
    value varchar(256) not null,
    primary key (dim_name, date),
    key (date)
);

DROP TABLE s_ge_daily_data;

SELECT * FROM s_ge_daily_data;