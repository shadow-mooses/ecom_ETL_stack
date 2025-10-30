with customer_base as (
select
   id as user_id,
   first_name as customer_first_name,
   last_name as customer_last_name
from
	{{ref('stg_customers')}}
),
sales_orders as (
select
	customer_id as user_id,
    count(product_id) as sales_per_customer
from
	{{ref('stg_sales_orders')}}
group by 1
)
select
	cb.user_id,
    cb.customer_first_name,
    cb.customer_last_name,
    so.sales_per_customer
from customer_base as cb
left join
	sales_orders as so
on
	cb.user_id = so.user_id