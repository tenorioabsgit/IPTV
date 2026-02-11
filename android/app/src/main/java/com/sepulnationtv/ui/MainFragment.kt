package com.sepulnationtv.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.leanback.app.BrowseSupportFragment
import androidx.leanback.widget.ArrayObjectAdapter
import androidx.leanback.widget.HeaderItem
import androidx.leanback.widget.ListRow
import androidx.leanback.widget.ListRowPresenter
import androidx.leanback.widget.OnItemViewClickedListener
import com.sepulnationtv.R
import com.sepulnationtv.data.PlaylistParser
import com.sepulnationtv.model.Channel
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.launch

class MainFragment : BrowseSupportFragment() {

    private val scope = CoroutineScope(Dispatchers.Main + SupervisorJob())

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        setupUI()
        loadPlaylist()
    }

    private fun setupUI() {
        title = "SepulnationTV"
        headersState = HEADERS_ENABLED
        isHeadersTransitionOnBackEnabled = true
        brandColor = ContextCompat.getColor(requireContext(), R.color.brand_color)

        onItemViewClickedListener = OnItemViewClickedListener { _, item, _, _ ->
            if (item is Channel) {
                val intent = Intent(requireContext(), PlayerActivity::class.java).apply {
                    putExtra(PlayerActivity.EXTRA_URL, item.url)
                    putExtra(PlayerActivity.EXTRA_TITLE, item.name)
                }
                startActivity(intent)
            }
        }
    }

    private fun loadPlaylist() {
        scope.launch {
            try {
                val grouped = PlaylistParser.loadPlaylist()
                val rowsAdapter = ArrayObjectAdapter(ListRowPresenter())

                grouped.forEach { (category, channels) ->
                    val cardPresenter = CardPresenter()
                    val listRowAdapter = ArrayObjectAdapter(cardPresenter)
                    channels.forEach { listRowAdapter.add(it) }

                    val header = HeaderItem(category)
                    rowsAdapter.add(ListRow(header, listRowAdapter))
                }

                adapter = rowsAdapter
            } catch (e: Exception) {
                Toast.makeText(
                    requireContext(),
                    "Erro ao carregar canais: ${e.message}",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }
}
