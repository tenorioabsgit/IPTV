import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/channel.dart';
import '../../providers/favorites_provider.dart';
import '../../providers/player_provider.dart';
import 'channel_logo.dart';

class ChannelCard extends ConsumerStatefulWidget {
  final Channel channel;

  const ChannelCard({super.key, required this.channel});

  @override
  ConsumerState<ChannelCard> createState() => _ChannelCardState();
}

class _ChannelCardState extends ConsumerState<ChannelCard> {
  bool _isFocused = false;

  @override
  Widget build(BuildContext context) {
    final playerState = ref.watch(playerProvider);
    final isPlaying = playerState.currentChannel?.url == widget.channel.url;
    final isFav = ref.watch(favoritesProvider).valueOrNull?.any(
              (c) => c.url == widget.channel.url,
            ) ??
        false;
    final colors = Theme.of(context).colorScheme;

    return AnimatedScale(
      scale: _isFocused ? 1.06 : 1.0,
      duration: const Duration(milliseconds: 200),
      curve: Curves.easeOut,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          border: _isFocused
              ? Border.all(color: colors.primary, width: 2.5)
              : isPlaying
                  ? Border.all(
                      color: colors.primary.withValues(alpha: 0.5), width: 1.5)
                  : Border.all(color: const Color(0xFF1E1E1E), width: 1),
          boxShadow: _isFocused
              ? [
                  BoxShadow(
                    color: colors.primary.withValues(alpha: 0.35),
                    blurRadius: 20,
                    spreadRadius: 2,
                  ),
                ]
              : null,
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(7),
          child: Material(
            color: const Color(0xFF1A1A1A),
            child: InkWell(
              onTap: () => ref
                  .read(playerProvider.notifier)
                  .playChannel(widget.channel),
              onFocusChange: (focused) {
                setState(() => _isFocused = focused);
              },
              child: Stack(
                fit: StackFit.expand,
                children: [
                  // Channel logo / background
                  _buildBackground(),
                  // Bottom gradient overlay
                  Positioned(
                    bottom: 0,
                    left: 0,
                    right: 0,
                    child: Container(
                      height: 64,
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [
                            Colors.transparent,
                            Color(0xDD000000),
                          ],
                        ),
                      ),
                    ),
                  ),
                  // Channel name at bottom
                  Positioned(
                    bottom: 8,
                    left: 10,
                    right: 10,
                    child: Text(
                      widget.channel.name,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(
                        color: _isFocused || isPlaying
                            ? Colors.white
                            : const Color(0xFFCCCCCC),
                        fontSize: 12,
                        fontWeight: _isFocused || isPlaying
                            ? FontWeight.w700
                            : FontWeight.w500,
                        shadows: const [
                          Shadow(blurRadius: 6, color: Colors.black),
                        ],
                      ),
                    ),
                  ),
                  // Playing badge
                  if (isPlaying)
                    Positioned(
                      top: 6,
                      right: 6,
                      child: Container(
                        padding: const EdgeInsets.symmetric(
                            horizontal: 6, vertical: 3),
                        decoration: BoxDecoration(
                          color: colors.primary,
                          borderRadius: BorderRadius.circular(4),
                        ),
                        child: const Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(Icons.play_arrow,
                                size: 10, color: Color(0xFF003544)),
                            SizedBox(width: 2),
                            Text(
                              'AO VIVO',
                              style: TextStyle(
                                fontSize: 8,
                                fontWeight: FontWeight.w800,
                                color: Color(0xFF003544),
                                letterSpacing: 0.5,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  // Favorite button
                  Positioned(
                    top: 6,
                    left: 6,
                    child: GestureDetector(
                      onTap: () => ref
                          .read(favoritesProvider.notifier)
                          .toggle(widget.channel),
                      child: Container(
                        padding: const EdgeInsets.all(5),
                        decoration: const BoxDecoration(
                          color: Color(0x88000000),
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          isFav ? Icons.favorite : Icons.favorite_border,
                          size: 14,
                          color: isFav
                              ? const Color(0xFFFF3333)
                              : const Color(0xAAFFFFFF),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildBackground() {
    final url = widget.channel.logoUrl;
    if (url != null && url.isNotEmpty) {
      return CachedNetworkImage(
        imageUrl: url,
        fit: BoxFit.contain,
        placeholder: (_, __) => _buildPlaceholder(),
        errorWidget: (_, __, ___) => _buildPlaceholder(),
      );
    }
    return _buildPlaceholder();
  }

  Widget _buildPlaceholder() {
    final name = widget.channel.name;
    return Container(
      color: const Color(0xFF141414),
      child: Center(
        child: Text(
          name.isNotEmpty ? name[0].toUpperCase() : '?',
          style: TextStyle(
            fontSize: 40,
            fontWeight: FontWeight.w800,
            color: _isFocused
                ? const Color(0xFF444444)
                : const Color(0xFF2A2A2A),
          ),
        ),
      ),
    );
  }
}

class ChannelListTile extends ConsumerStatefulWidget {
  final Channel channel;

  const ChannelListTile({super.key, required this.channel});

  @override
  ConsumerState<ChannelListTile> createState() => _ChannelListTileState();
}

class _ChannelListTileState extends ConsumerState<ChannelListTile> {
  bool _isFocused = false;

  @override
  Widget build(BuildContext context) {
    final playerState = ref.watch(playerProvider);
    final isPlaying = playerState.currentChannel?.url == widget.channel.url;
    final isFav = ref.watch(favoritesProvider).valueOrNull?.any(
              (c) => c.url == widget.channel.url,
            ) ??
        false;
    final colors = Theme.of(context).colorScheme;

    return AnimatedContainer(
      duration: const Duration(milliseconds: 150),
      margin: const EdgeInsets.symmetric(vertical: 1),
      decoration: BoxDecoration(
        border: _isFocused
            ? Border.all(color: colors.primary, width: 2)
            : isPlaying
                ? Border.all(
                    color: colors.primary.withValues(alpha: 0.4), width: 1)
                : null,
        borderRadius: BorderRadius.circular(8),
        boxShadow: _isFocused
            ? [
                BoxShadow(
                  color: colors.primary.withValues(alpha: 0.2),
                  blurRadius: 12,
                ),
              ]
            : null,
      ),
      child: ListTile(
        leading: ChannelLogo(logoUrl: widget.channel.logoUrl, size: 40),
        title: Text(
          widget.channel.name,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
          style: TextStyle(
            fontSize: 13,
            fontWeight:
                isPlaying || _isFocused ? FontWeight.bold : FontWeight.normal,
          ),
        ),
        subtitle: Text(
          widget.channel.group,
          style: TextStyle(
            fontSize: 11,
            color: colors.onSurfaceVariant,
          ),
        ),
        trailing: IconButton(
          icon: Icon(
            isFav ? Icons.favorite : Icons.favorite_border,
            size: 20,
            color: isFav ? colors.error : colors.onSurfaceVariant,
          ),
          onPressed: () =>
              ref.read(favoritesProvider.notifier).toggle(widget.channel),
        ),
        selected: isPlaying,
        selectedTileColor: colors.primaryContainer.withValues(alpha: 0.3),
        focusColor: colors.surfaceContainerHigh,
        tileColor: colors.surfaceContainerLow,
        onTap: () =>
            ref.read(playerProvider.notifier).playChannel(widget.channel),
        onFocusChange: (focused) {
          setState(() => _isFocused = focused);
        },
      ),
    );
  }
}
