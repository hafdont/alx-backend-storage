-- SCripts that lists bands by their longevity


SELECT origin, SUM(fans) AS nb_fans
	FROM metal_brands
	GROUP by origin
	ORDER BY nb_fans DESC;
