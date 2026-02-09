import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:media_kit_video/media_kit_video.dart';
import '../../../providers/player_provider.dart';
import '../../../providers/search_provider.dart';

class PlayerScreen extends ConsumerStatefulWidget {
  final VideoController videoController;

  const PlayerScreen({super.key, required this.videoController});

  @override
  ConsumerState<PlayerScreen> createState() => _PlayerScreenState();
}

class _PlayerScreenState extends ConsumerState<PlayerScreen> {
  bool _showOsd = true;
  Timer? _osdTimer;
  final FocusNode _focusNode = FocusNode();

  @override
  void initState() {
    super.initState();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.landscapeLeft,
      DeviceOrientation.landscapeRight,
    ]);
    _startOsdTimer();
  }

  @override
  void dispose() {
    _osdTimer?.cancel();
    _focusNode.dispose();
    SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge);
    super.dispose();
  }

  void _startOsdTimer() {
    _osdTimer?.cancel();
    setState(() => _showOsd = true);
    _osdTimer = Timer(const Duration(seconds: 3), () {
      if (mounted) setState(() => _showOsd = false);
    });
  }

  KeyEventResult _handleKeyEvent(FocusNode node, KeyEvent event) {
    if (event is! KeyDownEvent) return KeyEventResult.ignored;

    final key = event.logicalKey;
    final channels = ref.read(filteredChannelsProvider);
    final notifier = ref.read(playerProvider.notifier);

    if (key == LogicalKeyboardKey.channelUp ||
        key == LogicalKeyboardKey.arrowRight) {
      notifier.playNextChannel(channels);
      _startOsdTimer();
      return KeyEventResult.handled;
    }

    if (key == LogicalKeyboardKey.channelDown ||
        key == LogicalKeyboardKey.arrowLeft) {
      notifier.playPreviousChannel(channels);
      _startOsdTimer();
      return KeyEventResult.handled;
    }

    if (key == LogicalKeyboardKey.enter ||
        key == LogicalKeyboardKey.select ||
        key == LogicalKeyboardKey.mediaPlayPause ||
        key == LogicalKeyboardKey.mediaPlay ||
        key == LogicalKeyboardKey.mediaPause) {
      notifier.togglePlayPause();
      return KeyEventResult.handled;
    }

    if (key == LogicalKeyboardKey.goBack ||
        key == LogicalKeyboardKey.browserBack ||
        key == LogicalKeyboardKey.escape) {
      Navigator.of(context).pop();
      return KeyEventResult.handled;
    }

    if (key == LogicalKeyboardKey.mediaRewind) {
      notifier.playPreviousChannel(channels);
      _startOsdTimer();
      return KeyEventResult.handled;
    }
    if (key == LogicalKeyboardKey.mediaFastForward) {
      notifier.playNextChannel(channels);
      _startOsdTimer();
      return KeyEventResult.handled;
    }

    if (key == LogicalKeyboardKey.arrowUp ||
        key == LogicalKeyboardKey.arrowDown) {
      _startOsdTimer();
      return KeyEventResult.handled;
    }

    return KeyEventResult.ignored;
  }

  @override
  Widget build(BuildContext context) {
    final playerState = ref.watch(playerProvider);
    final channel = playerState.currentChannel;

    return PopScope(
      canPop: true,
      child: Scaffold(
        backgroundColor: Colors.black,
        body: Focus(
          focusNode: _focusNode,
          autofocus: true,
          onKeyEvent: _handleKeyEvent,
          child: Stack(
            children: [
              // Video
              Center(
                child: Video(
                  controller: widget.videoController,
                  controls: _noControls,
                ),
              ),

              // ===== OSD TOP - Channel info card =====
              if (channel != null)
                Positioned(
                  top: MediaQuery.of(context).padding.top + 20,
                  left: 24,
                  child: AnimatedOpacity(
                    opacity: _showOsd ? 1.0 : 0.0,
                    duration: const Duration(milliseconds: 400),
                    child: Container(
                      padding: const EdgeInsets.all(0),
                      decoration: BoxDecoration(
                        color: const Color(0xE60D0D0D),
                        borderRadius: BorderRadius.circular(8),
                        border: const Border(
                          left: BorderSide(
                            color: Color(0xFF00D4FF),
                            width: 3,
                          ),
                        ),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.fromLTRB(16, 12, 20, 12),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            // Channel name
                            Text(
                              channel.name,
                              style: const TextStyle(
                                color: Color(0xFFEEEEEE),
                                fontSize: 22,
                                fontWeight: FontWeight.w700,
                                shadows: [
                                  Shadow(
                                      blurRadius: 8, color: Colors.black),
                                ],
                              ),
                            ),
                            const SizedBox(height: 4),
                            // Category + Live indicator
                            Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text(
                                  channel.group,
                                  style: const TextStyle(
                                    color: Color(0xFF808080),
                                    fontSize: 13,
                                  ),
                                ),
                                const SizedBox(width: 12),
                                Container(
                                  width: 6,
                                  height: 6,
                                  decoration: const BoxDecoration(
                                    color: Color(0xFFFF3333),
                                    shape: BoxShape.circle,
                                  ),
                                ),
                                const SizedBox(width: 4),
                                const Text(
                                  'LIVE',
                                  style: TextStyle(
                                    color: Color(0xFFFF3333),
                                    fontSize: 10,
                                    fontWeight: FontWeight.w800,
                                    letterSpacing: 0.5,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),

              // ===== OSD BOTTOM - Control hints =====
              if (_showOsd)
                Positioned(
                  bottom: MediaQuery.of(context).padding.bottom + 16,
                  left: 0,
                  right: 0,
                  child: AnimatedOpacity(
                    opacity: _showOsd ? 1.0 : 0.0,
                    duration: const Duration(milliseconds: 400),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        _buildOsdChip(Icons.skip_previous_rounded, 'CH-'),
                        const SizedBox(width: 16),
                        _buildOsdChip(
                          playerState.isPlaying
                              ? Icons.pause_rounded
                              : Icons.play_arrow_rounded,
                          'OK',
                          accent: true,
                        ),
                        const SizedBox(width: 16),
                        _buildOsdChip(Icons.skip_next_rounded, 'CH+'),
                      ],
                    ),
                  ),
                ),

              // ===== ERROR OVERLAY =====
              if (playerState.error != null)
                Center(
                  child: Container(
                    padding: const EdgeInsets.all(32),
                    margin: const EdgeInsets.all(48),
                    decoration: BoxDecoration(
                      color: const Color(0xF0161616),
                      borderRadius: BorderRadius.circular(12),
                      border: const Border(
                        top: BorderSide(color: Color(0xFFFF3333), width: 3),
                      ),
                    ),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.error_outline,
                            color: Color(0xFFFF3333), size: 40),
                        const SizedBox(height: 16),
                        const Text(
                          'Erro ao reproduzir',
                          style: TextStyle(
                            color: Color(0xFFEEEEEE),
                            fontSize: 18,
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          playerState.error!,
                          style: const TextStyle(
                            color: Color(0xFF808080),
                            fontSize: 13,
                          ),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 20),
                        const Divider(
                          color: Color(0xFF2A2A2A),
                          height: 1,
                        ),
                        const SizedBox(height: 20),
                        FilledButton.icon(
                          onPressed: () {
                            if (channel != null) {
                              ref
                                  .read(playerProvider.notifier)
                                  .playChannel(channel);
                            }
                          },
                          icon: const Icon(Icons.refresh),
                          label: const Text('Tentar novamente'),
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildOsdChip(IconData icon, String label, {bool accent = false}) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      decoration: BoxDecoration(
        color: accent ? const Color(0xFF00D4FF) : const Color(0xCC0D0D0D),
        borderRadius: BorderRadius.circular(24),
        border: accent
            ? null
            : Border.all(color: const Color(0xFF333333), width: 1),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            color: accent ? const Color(0xFF003544) : const Color(0xFF808080),
            size: 18,
          ),
          const SizedBox(width: 6),
          Text(
            label,
            style: TextStyle(
              color:
                  accent ? const Color(0xFF003544) : const Color(0xFF808080),
              fontSize: 13,
              fontWeight: accent ? FontWeight.w700 : FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}

Widget _noControls(VideoState state) {
  return const SizedBox.shrink();
}
