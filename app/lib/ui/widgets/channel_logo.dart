import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

class ChannelLogo extends StatelessWidget {
  final String? logoUrl;
  final double size;
  final double borderRadius;

  const ChannelLogo({
    super.key,
    this.logoUrl,
    this.size = 48,
    this.borderRadius = 6,
  });

  @override
  Widget build(BuildContext context) {
    if (logoUrl == null || logoUrl!.isEmpty) {
      return _placeholder(context);
    }

    return ClipRRect(
      borderRadius: BorderRadius.circular(borderRadius),
      child: CachedNetworkImage(
        imageUrl: logoUrl!,
        width: size,
        height: size,
        fit: BoxFit.cover,
        placeholder: (context, url) => _placeholder(context),
        errorWidget: (context, url, error) => _placeholder(context),
      ),
    );
  }

  Widget _placeholder(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: const Color(0xFF1A1A1A),
        borderRadius: BorderRadius.circular(borderRadius),
        border: Border.all(color: const Color(0xFF2A2A2A), width: 1),
      ),
      child: Icon(
        Icons.tv,
        size: size * 0.45,
        color: const Color(0xFF444444),
      ),
    );
  }
}
