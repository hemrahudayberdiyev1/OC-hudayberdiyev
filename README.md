# Factorial, Deduplication and Linked List Reversal Services

## Overview

This project provides three industrial-grade microservices:

1. **Factorial Service** - Generates first n factorials
2. **Deduplication Service** - Removes duplicates from lists while preserving order
3. **Linked List Service** - Reverses linked lists using recursion

The services are implemented as REST APIs using FastAPI with comprehensive error handling, input validation, and complete test coverage.

## Features

- ✅ **Production-ready code** with proper error handling
- 🛡️ **Input validation** and sanitization
- 📊 **Comprehensive testing** (unit + integration)
- 📚 **Full API documentation** (Swagger UI included)
- ⚡ **Performance optimizations** with reasonable limits
- 🔍 **Type hints** throughout the codebase

## Services

### 1. Factorial Service

**Endpoint:** `GET /factorials/{n}`

Calculates first n factorials (1! to n!)

**Parameters:**
- `n`: Positive integer (1-10000)
