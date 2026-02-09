import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit_video/media_kit_video.dart';
import '../../providers/player_provider.dart';

class MiniPlayer extends ConsumerWidget {
  final VoidCallback onExpand;
  final VideoController videoController;

  const MiniPlayer({
    super.key,
    required this.onExpand,
    required this.videoController,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final playerState = ref.watch(playerProvider);
    final channel = playerState.currentChannel;
    if (channel == null) return const SizedBox.shrink();

    final colors = Theme.of(context).colorScheme;

    return Container(
      height: 64,
      decoration: BoxDecoration(
        color: const Color(0xFF141414),
        border: Border(
          top: BorderSide(
            color: colors.primary.withValues(alpha: 0.3),
            width: 1,
          ),
        ),
      ),
      child: Row(
        children: [
          // Mini video preview
          SizedBox(
            width: 100,
            height: 64,
            child: Video(
              controller: videoController,
              controls: NoVideoControls,
            ),
          ),
          // Accent separator
          Container(
            width: 2,
            height: 36,
            color: colors.primary.withValues(alpha: 0.5),
          ),
          const SizedBox(width: 12),
          // Channel info
          Expanded(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  channel.name,
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    fontWeight: FontWeight.w600,
                    fontSize: 13,
                    color: Color(0xFFE5E5E5),
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  channel.group,
                  style: const TextStyle(
                    fontSize: 11,
                    color: Color(0xFF808080),
                  ),
                ),
              ],
            ),
          ),
          // Controls
          if (playerState.isBuffering)
            const Padding(
              padding: EdgeInsets.all(12),
              child: SizedBox(
                width: 22,
                height: 22,
                child: CircularProgressIndicator(strokeWidth: 2),
              ),
            )
          else
            IconButton(
              icon: Icon(
                playerState.isPlaying ? Icons.pause : Icons.play_arrow,
                color: colors.primary,
              ),
              onPressed: () {
                final player = ref.read(playerProvider.notifier).player;
                player.playOrPause();
              },
            ),
          IconButton(
            icon: const Icon(Icons.stop, color: Color(0xFF808080)),
            onPressed: () => ref.read(playerProvider.notifier).stop(),
          ),
          IconButton(
            icon: Icon(Icons.fullscreen, color: colors.primary),
            onPressed: onExpand,
          ),
          const SizedBox(width: 4),
        ],
      ),
    );
  }
}

Widget NoVideoControls(VideoState state) {
  return const SizedBox.shrink();
}
