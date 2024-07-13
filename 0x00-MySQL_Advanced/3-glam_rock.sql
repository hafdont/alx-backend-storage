-- Script to list bands

SELECT band_name, (2022 - formed) - IFNULL((2022 - SPLIT), 0) AS lifespan
	FROM metal_bands
	WHERE main_style = 'Glam rock'
	ORDERBY lifespan DESC;
