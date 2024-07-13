-- SCripts that lists bands by their longevity

SELECT origin, SUM(nb_fans)AS nb_fans
FROM metal_brands
GROUP by origin
ORDER BY nb_fans DESC;
