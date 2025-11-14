package com.example.shopping.data.remote

import com.example.shopping.domain.model.ProductCatalog
import kotlinx.serialization.Serializable

// SPEC-002: Data transfer object
@Serializable
data class ProductCatalogDto(
    val id: String,
    // TODO: Add fields based on SPEC
)

// SPEC-002: Mapper from DTO to Domain
fun ProductCatalogDto.toDomain(): ProductCatalog = ProductCatalog(
    id = id,
    // TODO: Map fields
)
