package com.sepulnationtv.ui

import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.leanback.widget.ImageCardView
import androidx.leanback.widget.Presenter
import com.bumptech.glide.Glide
import com.sepulnationtv.R
import com.sepulnationtv.model.Channel

class CardPresenter : Presenter() {

    companion object {
        private const val CARD_WIDTH = 320
        private const val CARD_HEIGHT = 180
    }

    override fun onCreateViewHolder(parent: ViewGroup): ViewHolder {
        val cardView = ImageCardView(parent.context).apply {
            isFocusable = true
            isFocusableInTouchMode = true
            setMainImageDimensions(CARD_WIDTH, CARD_HEIGHT)
            setBackgroundColor(
                ContextCompat.getColor(context, R.color.card_background)
            )
        }
        return ViewHolder(cardView)
    }

    override fun onBindViewHolder(viewHolder: ViewHolder, item: Any) {
        val channel = item as Channel
        val cardView = viewHolder.view as ImageCardView

        cardView.titleText = channel.name
        cardView.contentText = channel.group

        if (channel.logo.isNotEmpty()) {
            Glide.with(cardView.context)
                .load(channel.logo)
                .centerCrop()
                .error(R.color.card_background)
                .into(cardView.mainImageView)
        }
    }

    override fun onUnbindViewHolder(viewHolder: ViewHolder) {
        val cardView = viewHolder.view as ImageCardView
        cardView.badgeImage = null
        cardView.mainImage = null
    }
}
