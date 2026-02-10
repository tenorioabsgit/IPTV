sub Init()
    m.poster = m.top.FindNode("poster")
    m.titleLabel = m.top.FindNode("titleLabel")
    m.categoryLabel = m.top.FindNode("categoryLabel")
    m.streamInfoLabel = m.top.FindNode("streamInfoLabel")
    m.buttons = m.top.FindNode("buttons")
end sub

sub OnContentSet()
    content = m.top.content
    if content = invalid then return

    m.titleLabel.text = content.title

    if content.description <> invalid and content.description <> ""
        m.categoryLabel.text = CleanCategoryTitle(content.description)
    else
        m.categoryLabel.text = ""
    end if

    if content.hdPosterUrl <> invalid and content.hdPosterUrl <> ""
        m.poster.uri = content.hdPosterUrl
    end if

    ' Stream info
    fmt = "HLS"
    if content.streamFormat <> invalid and content.streamFormat <> ""
        fmt = UCase(content.streamFormat)
    end if
    m.streamInfoLabel.text = "Formato: " + fmt

    ' Button content
    buttonContent = CreateObject("roSGNode", "ContentNode")
    playBtn = buttonContent.CreateChild("ContentNode")
    playBtn.title = "Assistir agora"
    m.buttons.content = buttonContent

    m.buttons.SetFocus(true)
end sub

function OnKeyEvent(key as String, press as Boolean) as Boolean
    if not press then return false
    return false
end function
