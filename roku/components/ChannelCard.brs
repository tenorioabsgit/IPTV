sub init()
    m.focusBorder = m.top.findNode("focusBorder")
    m.cardBg = m.top.findNode("cardBg")
    m.poster = m.top.findNode("poster")
    m.noPosterBg = m.top.findNode("noPosterBg")
    m.noPosterLetter = m.top.findNode("noPosterLetter")
    m.gradientOverlay = m.top.findNode("gradientOverlay")
    m.channelName = m.top.findNode("channelName")
end sub

sub onContentChange()
    content = m.top.itemContent
    if content = invalid then return

    title = content.title
    m.channelName.text = title

    hasPoster = false
    if content.hdPosterUrl <> invalid and content.hdPosterUrl <> ""
        hasPoster = true
    end if

    if hasPoster
        m.poster.uri = content.hdPosterUrl
        m.poster.visible = true
        m.noPosterBg.visible = false
        m.gradientOverlay.visible = true
    else
        m.poster.visible = false
        m.noPosterBg.visible = true
        m.gradientOverlay.visible = true

        ' Show first letter as large initial
        if len(title) > 0
            m.noPosterLetter.text = left(title, 1)
        else
            m.noPosterLetter.text = "?"
        end if
    end if
end sub

sub onFocusChange()
    fp = m.top.focusPercent

    ' Animate focus border opacity
    m.focusBorder.opacity = fp

    ' Dim unfocused cards slightly for depth effect
    m.cardBg.opacity = 0.65 + (fp * 0.35)
end sub
