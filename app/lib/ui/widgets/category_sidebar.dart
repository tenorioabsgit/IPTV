import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/models/channel_group.dart';
import '../../providers/playlist_provider.dart';
import '../../providers/search_provider.dart';

class CategorySidebar extends ConsumerWidget {
  const CategorySidebar({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final playlistState = ref.watch(playlistProvider);
    final selectedCategory = ref.watch(selectedCategoryProvider);

    return playlistState.when(
      data: (data) =>
          _buildList(context, ref, data.groups, selectedCategory),
      loading: () => const Center(
        child: CircularProgressIndicator(strokeWidth: 2),
      ),
      error: (e, _) => Center(
        child: Text('Erro: $e', style: const TextStyle(fontSize: 12)),
      ),
    );
  }

  Widget _buildList(
    BuildContext context,
    WidgetRef ref,
    List<ChannelGroup> groups,
    String? selectedCategory,
  ) {
    final totalChannels =
        groups.fold<int>(0, (sum, g) => sum + g.count);

    return ListView(
      padding: const EdgeInsets.symmetric(vertical: 8),
      children: [
        // "All channels" option
        _CategoryTile(
          icon: Icons.tv,
          label: 'Todos',
          count: totalChannels,
          isSelected: selectedCategory == null,
          onTap: () =>
              ref.read(selectedCategoryProvider.notifier).state = null,
        ),
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 20, vertical: 4),
          child: Divider(height: 1),
        ),
        // Group categories
        for (final group in groups)
          _CategoryTile(
            icon: _iconForGroup(group.name),
            label: group.name,
            count: group.count,
            isSelected: selectedCategory == group.name,
            onTap: () => ref.read(selectedCategoryProvider.notifier).state =
                group.name,
          ),
      ],
    );
  }

  static IconData _iconForGroup(String name) {
    final lower = name.toLowerCase();
    if (lower.contains('not\u00edcia') || lower.contains('news')) {
      return Icons.newspaper;
    }
    if (lower.contains('esporte') || lower.contains('sport')) {
      return Icons.sports_soccer;
    }
    if (lower.contains('filme') || lower.contains('movie')) {
      return Icons.movie;
    }
    if (lower.contains('s\u00e9rie')) return Icons.video_library;
    if (lower.contains('anime')) return Icons.animation;
    if (lower.contains('kid') || lower.contains('infantil')) {
      return Icons.child_care;
    }
    if (lower.contains('religi')) return Icons.church;
    if (lower.contains('legisl')) return Icons.account_balance;
    if (lower.contains('m\u00fasic') || lower.contains('music')) {
      return Icons.music_note;
    }
    if (lower.contains('mtv')) return Icons.music_video;
    if (lower.contains('vh1')) return Icons.audiotrack;
    if (lower.contains('entret')) return Icons.theater_comedy;
    if (lower.contains('varied')) return Icons.dashboard;
    if (lower.contains('usa') ||
        lower.contains('uk') ||
        lower.contains('canada')) {
      return Icons.public;
    }
    return Icons.live_tv;
  }
}

class _CategoryTile extends StatefulWidget {
  final IconData icon;
  final String label;
  final int count;
  final bool isSelected;
  final VoidCallback onTap;

  const _CategoryTile({
    required this.icon,
    required this.label,
    required this.count,
    required this.isSelected,
    required this.onTap,
  });

  @override
  State<_CategoryTile> createState() => _CategoryTileState();
}

class _CategoryTileState extends State<_CategoryTile> {
  bool _isFocused = false;

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    final isActive = widget.isSelected || _isFocused;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 1),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 150),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          color: widget.isSelected
              ? colors.primary.withValues(alpha: 0.12)
              : _isFocused
                  ? colors.surfaceContainerHigh
                  : Colors.transparent,
          border: _isFocused && !widget.isSelected
              ? Border.all(color: colors.primary.withValues(alpha: 0.4), width: 1)
              : null,
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(8),
          onTap: widget.onTap,
          onFocusChange: (f) => setState(() => _isFocused = f),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
            child: Row(
              children: [
                // Accent indicator bar
                AnimatedContainer(
                  duration: const Duration(milliseconds: 200),
                  width: 3,
                  height: 20,
                  margin: const EdgeInsets.only(right: 10),
                  decoration: BoxDecoration(
                    color: widget.isSelected
                        ? colors.primary
                        : Colors.transparent,
                    borderRadius: BorderRadius.circular(2),
                  ),
                ),
                Icon(
                  widget.icon,
                  size: 18,
                  color: isActive
                      ? colors.primary
                      : colors.onSurfaceVariant,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    widget.label,
                    style: TextStyle(
                      fontSize: 13,
                      fontWeight:
                          isActive ? FontWeight.w600 : FontWeight.normal,
                      color: isActive
                          ? colors.onSurface
                          : colors.onSurfaceVariant,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
                  decoration: BoxDecoration(
                    color: widget.isSelected
                        ? colors.primary.withValues(alpha: 0.2)
                        : const Color(0xFF222222),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(
                    '${widget.count}',
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                      color: widget.isSelected
                          ? colors.primary
                          : const Color(0xFF666666),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
