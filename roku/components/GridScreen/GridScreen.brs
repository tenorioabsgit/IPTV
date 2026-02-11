' GridScreen - channel browsing grid
' Based on GridScreen from SceneGraph Master Sample
sub Init()
    m.rowList = m.top.FindNode("rowList")
    m.descriptionLabel = m.top.FindNode("descriptionLabel")
    m.titleLabel = m.top.FindNode("titleLabel")
    m.top.ObserveField("visible", "OnVisibleChange")
    m.rowList.ObserveField("rowItemFocused", "OnItemFocused")
    m.rowList.ObserveField("content", "OnContentLoaded")
end sub

sub OnContentLoaded()
    if m.rowList.content <> invalid
        m.rowList.SetFocus(true)
    end if
end sub

sub OnVisibleChange()
    if m.top.visible = true and m.rowList.content <> invalid
        m.rowList.SetFocus(true)
    end if
end sub

sub OnItemFocused()
    focusedIndex = m.rowList.rowItemFocused
    if m.rowList.content = invalid then return
    row = m.rowList.content.GetChild(focusedIndex[0])
    if row = invalid then return
    item = row.GetChild(focusedIndex[1])
    if item = invalid then return
    m.descriptionLabel.text = item.description
    m.titleLabel.text = item.title
end sub
