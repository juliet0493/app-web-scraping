with aggr_sales as (
	SELECT distinct 
		DATE_PART('year', o.date::date) as year, 
		DATE_PART('month', o.date::date) as month,
		o.customer_id,
		o.order_id,
		o.order_item_id,
		o.product_id,
		p.subcategory,
		cast(o.nsbr_amount as decimal(32,2)) as payment_amount,
		cast(o.qty_ordered-o.qty_returned as int) as qty
	FROM public.order_items o
	LEFT JOIN public.products p on o.product_id = p.product_id
	where o.nsbr_amount > 0 or o.coupon_code_amount > 0
),
product_seq as (
	SELECT  
		year, 
		month,
		product_id,
		sum(qty) as total_qty,
		row_number() over (partition by month order by sum(qty) desc) as sequence
	FROM aggr_sales 
	group by year, month, product_id
)
SELECT * FROM product_seq where sequence <= 3;