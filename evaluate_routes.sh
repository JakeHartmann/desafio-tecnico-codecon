#!/bin/bash

set -e

declare -A totals
declare -A counts

echo "==> Coletando rotas disponíveis"
routes=$(curl -s http://localhost:5000/evaluation | jq -r '.tested_endpoints | keys[]')

for i in {1..5}; do
    eval=$(curl -s http://localhost:5000/evaluation)
    for route in $routes; do
        time=$(echo "$eval" | jq ".tested_endpoints[\"$route\"].time_ms")
        totals["$route"]=$(echo "${totals[$route]:-0} + $time" | bc)
        counts["$route"]=$((counts["$route"] + 1))
    done
done

echo ""
echo "==> Média de tempo via /evaluation (interno):"
for route in "${!totals[@]}"; do
    avg=$(echo "scale=2; ${totals[$route]} / ${counts[$route]}" | bc)
    echo "$route: ${avg}ms"
done

echo ""
echo "==> Média de tempo via curl:"
for route in $routes; do
    total=0
    for i in {1..5}; do
        t=$(curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:5000$route")
        t_ms=$(echo "$t * 1000" | bc)
        total=$(echo "$total + $t_ms" | bc)
    done
    avg=$(echo "scale=2; $total / 5" | bc)
    echo "$route: ${avg}ms"
done
