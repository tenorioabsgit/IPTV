sub Init()
    m.rowList = m.top.FindNode("rowList")
    m.loadingGroup = m.top.FindNode("loadingGroup")
    m.heroGroup = m.top.FindNode("heroGroup")
    m.heroPoster = m.top.FindNode("heroPoster")
    m.heroChannelName = m.top.FindNode("heroChannelName")
    m.heroCategory = m.top.FindNode("heroCategory")
    m.channelCount = m.top.FindNode("channelCount")

    m.rowList.ObserveField("rowItemFocused", "OnRowItemFocused")
end sub

sub OnContentChange()
    content = m.top.content
    if content = invalid then return

    m.loadingGroup.visible = false
    m.heroGroup.visible = true
    m.rowList.visible = true
    m.rowList.content = content

    ' Count total channels
    totalChannels = 0
    if content.GetChildCount() > 0
        allCat = content.GetChild(0)
        totalChannels = allCat.GetChildCount()
    end if
    m.channelCount.text = IntToStr(totalChannels)

    ' Show first channel in hero
    if content.GetChildCount() > 0 and content.GetChild(0).GetChildCount() > 0
        UpdateHero(content.GetChild(0).GetChild(0), content.GetChild(0).title)
    end if

    m.rowList.SetFocus(true)
end sub

sub OnRowItemFocused()
    focused = m.rowList.rowItemFocused
    if focused = invalid then return

    rowIndex = focused[0]
    itemIndex = focused[1]

    content = m.top.content
    if content = invalid then return
    if rowIndex < 0 or rowIndex >= content.GetChildCount() then return

    row = content.GetChild(rowIndex)
    if itemIndex < 0 or itemIndex >= row.GetChildCount() then return

    UpdateHero(row.GetChild(itemIndex), row.title)
end sub

sub UpdateHero(channelNode as Object, categoryTitle as String)
    m.heroChannelName.text = channelNode.title
    m.heroCategory.text = CleanCategoryTitle(categoryTitle)

    if channelNode.hdPosterUrl <> invalid and channelNode.hdPosterUrl <> ""
        m.heroPoster.uri = channelNode.hdPosterUrl
    else
        m.heroPoster.uri = ""
    end if
end sub

function OnKeyEvent(key as String, press as Boolean) as Boolean
    if not press then return false
    return false
end function
