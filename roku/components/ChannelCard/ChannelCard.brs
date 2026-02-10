sub Init()
    m.focusBorder = m.top.FindNode("focusBorder")
    m.cardBg = m.top.FindNode("cardBg")
    m.poster = m.top.FindNode("poster")
    m.noPosterBg = m.top.FindNode("noPosterBg")
    m.noPosterLetter = m.top.FindNode("noPosterLetter")
    m.channelName = m.top.FindNode("channelName")
end sub

sub OnContentChange()
    content = m.top.itemContent
    if content = invalid then return

    title = content.title
    m.channelName.text = title

    hasPoster = (content.hdPosterUrl <> invalid and content.hdPosterUrl <> "")

    if hasPoster
        m.poster.uri = content.hdPosterUrl
        m.poster.visible = true
        m.noPosterBg.visible = false
    else
        m.poster.visible = false
        m.noPosterBg.visible = true
        if Len(title) > 0
            m.noPosterLetter.text = Left(title, 1)
        else
            m.noPosterLetter.text = "?"
        end if
    end if
end sub

sub OnFocusChange()
    fp = m.top.focusPercent
    m.focusBorder.opacity = fp
    m.cardBg.opacity = 0.65 + (fp * 0.35)
end sub
