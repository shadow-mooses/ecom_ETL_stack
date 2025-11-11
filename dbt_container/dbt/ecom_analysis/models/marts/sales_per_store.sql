with sales_per_store as (
select
   so.store_id,
   so.product_id,
   po.product_price,
   st.store_name
from {{ref('stg_sales_orders')}} as so
join {{ref('stg_products')}} as po
on so.product_id = po.id
join {{ref('_stores')}} as st
on so.store_id = st.store_id
where so.order_status = 'Delivered')

select
  store_name as store_name,
  sum(product_price) as total_sales
from sales_per_store
group by 1
order by 2 desc
