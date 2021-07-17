#!/bin/bash
echo "Running Unit Tests"
cd ".." && cd "test" && pytest -rP
