package com.example.shopping.domain.repository

import com.example.shopping.domain.model.ProductCatalog

// SPEC-002: Repository interface
interface ProductCatalogRepository {
    suspend fun getProductCatalog(id: String): Result<ProductCatalog>
    // TODO: Add methods based on SPEC requirements
}
