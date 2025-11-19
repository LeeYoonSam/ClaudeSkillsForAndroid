---
name: android-xml-views
description: Build UI with XML layouts, ViewBinding, and View components for legacy or gradual migration projects. Use when working with existing XML-based apps.
---

# Android XML Views

Build UI with XML layouts using ViewBinding and traditional Android Views.

## When to Use
- Working with legacy XML-based apps
- Gradual migration from XML to Compose
- Maintaining existing codebase
- Using Views not yet available in Compose

## ViewBinding Setup

### Enable ViewBinding

```kotlin
// build.gradle.kts
android {
    buildFeatures {
        viewBinding = true
    }
}
```

### Using ViewBinding in Activity

```kotlin
class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.textView.text = "Hello"
        binding.button.setOnClickListener {
            // Handle click
        }
    }
}
```

### Using ViewBinding in Fragment

```kotlin
class HomeFragment : Fragment() {
    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.recyclerView.adapter = myAdapter
        binding.button.setOnClickListener { }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
```

## Common Layouts

### LinearLayout

```xml
<LinearLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:orientation="vertical"
    android:padding="16dp">

    <TextView
        android:id="@+id/titleText"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:text="Title"
        android:textSize="24sp" />

    <Button
        android:id="@+id/actionButton"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="Action" />

</LinearLayout>
```

### ConstraintLayout

```xml
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ImageView
        android:id="@+id/imageView"
        android:layout_width="64dp"
        android:layout_height="64dp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />

    <TextView
        android:id="@+id/nameText"
        android:layout_width="0dp"
        android:layout_height="wrap_content"
        android:layout_marginStart="16dp"
        app:layout_constraintStart_toEndOf="@id/imageView"
        app:layout_constraintTop_toTopOf="@id/imageView"
        app:layout_constraintEnd_toEndOf="parent" />

</androidx.constraintlayout.widget.ConstraintLayout>
```

## RecyclerView

### Adapter

```kotlin
class ProductAdapter(
    private val onItemClick: (Product) -> Unit
) : RecyclerView.Adapter<ProductAdapter.ViewHolder>() {

    private var items = listOf<Product>()

    fun submitList(newItems: List<Product>) {
        items = newItems
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemProductBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return ViewHolder(binding)
    }

    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        holder.bind(items[position])
    }

    override fun getItemCount() = items.size

    inner class ViewHolder(
        private val binding: ItemProductBinding
    ) : RecyclerView.ViewHolder(binding.root) {

        init {
            binding.root.setOnClickListener {
                val position = bindingAdapterPosition
                if (position != RecyclerView.NO_POSITION) {
                    onItemClick(items[position])
                }
            }
        }

        fun bind(product: Product) {
            binding.nameText.text = product.name
            binding.priceText.text = "$${product.price}"
            Glide.with(binding.root.context)
                .load(product.imageUrl)
                .into(binding.imageView)
        }
    }
}
```

### Setup RecyclerView

```kotlin
class ProductListFragment : Fragment() {
    private var _binding: FragmentProductListBinding? = null
    private val binding get() = _binding!!

    private val adapter = ProductAdapter { product ->
        // Handle item click
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.recyclerView.apply {
            layoutManager = LinearLayoutManager(context)
            adapter = this@ProductListFragment.adapter
            addItemDecoration(
                DividerItemDecoration(context, DividerItemDecoration.VERTICAL)
            )
        }
    }
}
```

## ViewModel Integration

```kotlin
@AndroidEntryPoint
class HomeFragment : Fragment() {
    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private val viewModel: HomeViewModel by viewModels()

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Observe state
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.state.collect { state ->
                    updateUI(state)
                }
            }
        }

        // Observe events
        viewLifecycleOwner.lifecycleScope.launch {
            viewLifecycleOwner.repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.events.collect { event ->
                    handleEvent(event)
                }
            }
        }
    }

    private fun updateUI(state: HomeState) {
        binding.progressBar.isVisible = state.isLoading
        binding.errorView.isVisible = state.error != null
        adapter.submitList(state.items)
    }

    private fun handleEvent(event: HomeEvent) {
        when (event) {
            is HomeEvent.ShowMessage -> {
                Snackbar.make(binding.root, event.message, Snackbar.LENGTH_SHORT).show()
            }
        }
    }
}
```

## Related Skills
- **android-mvvm-architecture**: For ViewModel patterns
- **android-compose-ui**: For migrating to Compose

## Best Practices
1. Always use ViewBinding instead of findViewById
2. Set binding to null in Fragment's onDestroyView
3. Use ConstraintLayout for complex layouts
4. Use RecyclerView for lists, not ListView
5. Collect StateFlow with repeatOnLifecycle
