#!/bin/bash

generate_password() {
    local length=$1
    local charset='a-zA-Z0-9!@#$%^&*()_+-=[]{}|;:,.<>?~'
    local password=$(cat /dev/urandom 2>/dev/null | LC_ALL=C tr -dc "$charset" | fold -w "$length" | head -n 1)
    
    if [[ -z "$password" ]]; then
        echo "Error: failed to generate password" >&2
        return 1
    fi
    
    echo "$password"
    return 0
}

DEFAULT_LENGTH=12
password_length=$DEFAULT_LENGTH

if [[ $# -gt 1 ]]; then
    echo "Error: too many arguments" >&2
    exit 1
fi

if [[ $# -eq 1 ]]; then
    arg="$1"
    
    if [[ "$arg" == "-h" ]] || [[ "$arg" == "--help" ]]; then
        echo "Usage: $0 [LENGTH]"
        echo "LENGTH - positive integer from 1 to 256 (default: 12)"
        exit 0
    fi
    
    if [[ ! "$arg" =~ ^[0-9]+$ ]]; then
        echo "Error: length must be a number" >&2
        exit 1
    fi
    
    if [[ "$arg" -lt 1 ]] || [[ "$arg" -gt 256 ]]; then
        echo "Error: length must be between 1 and 256" >&2
        exit 1
    fi
    
    password_length="$arg"
fi

generated_password=$(generate_password "$password_length")

if [[ $? -ne 0 ]]; then
    exit 1
fi

echo "$generated_password"
