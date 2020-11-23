#!/bin/bash
echo "Running Unit Tests"
cd ".." && cd "test" && find . -name 'test_*py' -exec python '{}' \;
