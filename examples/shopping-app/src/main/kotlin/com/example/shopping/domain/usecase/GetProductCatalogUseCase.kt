package com.example.shopping.domain.usecase

import com.example.shopping.domain.model.ProductCatalog
import com.example.shopping.domain.repository.ProductCatalogRepository
import javax.inject.Inject

// SPEC-002: Get ProductCatalog use case
class GetProductCatalogUseCase @Inject constructor(
    private val repository: ProductCatalogRepository
) {
    suspend operator fun invoke(id: String): Result<ProductCatalog> {
        return repository.getProductCatalog(id)
    }
}
