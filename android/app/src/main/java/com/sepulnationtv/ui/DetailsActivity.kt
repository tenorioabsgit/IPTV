package com.sepulnationtv.ui

import android.content.Intent
import android.os.Bundle
import android.view.KeyEvent
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import androidx.fragment.app.FragmentActivity
import com.bumptech.glide.Glide
import com.sepulnationtv.R
import com.sepulnationtv.data.ChannelRepository
import com.sepulnationtv.model.Channel

class DetailsActivity : FragmentActivity() {

    private lateinit var posterView: ImageView
    private lateinit var titleView: TextView
    private lateinit var formatView: TextView
    private lateinit var categoryView: TextView
    private lateinit var watchButton: Button
    private lateinit var prevButton: Button
    private lateinit var nextButton: Button
    private lateinit var counterView: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_details)

        posterView = findViewById(R.id.channel_poster)
        titleView = findViewById(R.id.channel_title)
        formatView = findViewById(R.id.channel_format)
        categoryView = findViewById(R.id.channel_category)
        watchButton = findViewById(R.id.watch_button)
        prevButton = findViewById(R.id.prev_button)
        nextButton = findViewById(R.id.next_button)
        counterView = findViewById(R.id.channel_counter)

        watchButton.setOnClickListener { playChannel() }

        prevButton.setOnClickListener {
            if (ChannelRepository.currentIndex > 0) {
                ChannelRepository.currentIndex--
                updateChannel()
            }
        }

        nextButton.setOnClickListener {
            if (ChannelRepository.currentIndex < ChannelRepository.currentChannels.size - 1) {
                ChannelRepository.currentIndex++
                updateChannel()
            }
        }

        updateChannel()
    }

    private fun currentChannel(): Channel {
        return ChannelRepository.currentChannels[ChannelRepository.currentIndex]
    }

    private fun updateChannel() {
        val channel = currentChannel()
        val index = ChannelRepository.currentIndex
        val total = ChannelRepository.currentChannels.size

        titleView.text = channel.name
        formatView.text = "Formato: ${channel.streamFormat}"
        categoryView.text = "Categoria: ${channel.group}"
        counterView.text = "${index + 1} / $total"

        prevButton.isEnabled = index > 0
        nextButton.isEnabled = index < total - 1

        if (channel.logo.isNotEmpty()) {
            Glide.with(this)
                .load(channel.logo)
                .centerCrop()
                .error(R.color.card_background)
                .into(posterView)
        } else {
            posterView.setImageResource(R.color.card_background)
        }
    }

    private fun playChannel() {
        val channel = currentChannel()
        val intent = Intent(this, PlayerActivity::class.java).apply {
            putExtra(PlayerActivity.EXTRA_URL, channel.url)
            putExtra(PlayerActivity.EXTRA_TITLE, channel.name)
        }
        startActivity(intent)
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent?): Boolean {
        when (keyCode) {
            KeyEvent.KEYCODE_DPAD_LEFT -> {
                if (ChannelRepository.currentIndex > 0) {
                    ChannelRepository.currentIndex--
                    updateChannel()
                    return true
                }
            }
            KeyEvent.KEYCODE_DPAD_RIGHT -> {
                if (ChannelRepository.currentIndex < ChannelRepository.currentChannels.size - 1) {
                    ChannelRepository.currentIndex++
                    updateChannel()
                    return true
                }
            }
            KeyEvent.KEYCODE_MEDIA_PLAY, KeyEvent.KEYCODE_ENTER, KeyEvent.KEYCODE_DPAD_CENTER -> {
                playChannel()
                return true
            }
        }
        return super.onKeyDown(keyCode, event)
    }
}
