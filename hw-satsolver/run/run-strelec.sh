#!/bin/bash
../strelec/target/release/solve $1 | tr -d "{,}" > $2
