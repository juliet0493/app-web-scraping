SELECT DISTINCT
	customer_id
FROM public.order_items
where (nsbr_amount > 0 or coupon_code_amount > 0) 
and customer_id not in (
	SELECT
		o.customer_id
	FROM public.order_items o
	LEFT JOIN public.products p on o.product_id = p.product_id
	where p.subcategory = 'pants'
);