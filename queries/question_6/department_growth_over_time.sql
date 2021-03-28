select season as SEASON, count(season) as UNITS_SOLD_DURING_SEASON, p.DEPARTMENT /*, SUM(t.UNITS) */
from (
    select PURCHASE,
    case
        when PURCHASE between '2018-03-21' and '2018-06-20' then 'spring_18'
        when PURCHASE between '2019-03-21' and '2019-06-20' then 'spring_19'
        when PURCHASE between '2018-06-21' and '2018-09-22' then 'summer_18'
        when PURCHASE between '2019-06-21' and '2019-09-22' then 'summer_19'
        when PURCHASE between '2018-09-23' and '2018-12-20' then 'fall_18'
        when PURCHASE between '2019-09-23' and '2019-12-20' then 'fall_19'
        else                                                     'winter_19'
    end as SEASON
    from dbo.transactions
) purchases_by_season,
transactions t,
products p
where t.PRODUCT_NUM = p.PRODUCT_NUM
group by season, p.DEPARTMENT
order by case season
    when 'summer_18' then 1
    when 'fall_18' then 2
    when 'winter_19' then 3
    when 'spring_19' then 4
    when 'summer_19' then 5
    else 6
end, p.DEPARTMENT desc;
