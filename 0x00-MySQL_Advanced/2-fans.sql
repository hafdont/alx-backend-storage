-- SCripts that lists bands by their longevity


SELECT origin, SUM(nb_fans) AS nb_fans
	FROM metal_bands
	GROUP by origin
	ORDER BY nbfans DESC;
