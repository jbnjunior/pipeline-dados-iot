-- View 1: média, mínima, máxima e quantidade de leituras por dispositivo.
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    ROUND(MIN(temperature)::numeric, 2) AS min_temp,
    ROUND(MAX(temperature)::numeric, 2) AS max_temp,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY device_id;

-- View 2: quantidade de leituras por hora do dia (0 a 23).
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM recorded_at)::integer AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
GROUP BY EXTRACT(HOUR FROM recorded_at)::integer
ORDER BY hora;

-- View 3: temperatura máxima e mínima por dia.
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(recorded_at) AS data,
    ROUND(MAX(temperature)::numeric, 2) AS temp_max,
    ROUND(MIN(temperature)::numeric, 2) AS temp_min,
    ROUND(AVG(temperature)::numeric, 2) AS temp_media,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY DATE(recorded_at)
ORDER BY data;

-- View adicional: quantidade de registros e período coberto pelo dataset.
CREATE OR REPLACE VIEW resumo_dataset AS
SELECT
    COUNT(*) AS total_leituras,
    COUNT(DISTINCT device_id) AS total_dispositivos,
    MIN(recorded_at) AS primeira_leitura,
    MAX(recorded_at) AS ultima_leitura
FROM temperature_readings;
