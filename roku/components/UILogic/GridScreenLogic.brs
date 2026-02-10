' GridScreenLogic.brs - Grid selection handling
' Based on SceneGraph Master Sample pattern

sub InitGridScreenLogic()
    m.gridScreen.ObserveField("rowItemSelected", "OnGridItemSelected")
end sub

sub OnGridItemSelected()
    selected = m.gridScreen.rowItemSelected
    if selected = invalid then return

    rowIndex = selected[0]
    itemIndex = selected[1]

    if m.allContent = invalid then return
    if rowIndex < 0 or rowIndex >= m.allContent.GetChildCount() then return

    row = m.allContent.GetChild(rowIndex)
    if itemIndex < 0 or itemIndex >= row.GetChildCount() then return

    channelNode = row.GetChild(itemIndex)

    ' Update channel index for CH+/CH-
    for i = 0 to m.allChannels.Count() - 1
        if m.allChannels[i].url = channelNode.url
            m.currentChannelIndex = i
            exit for
        end if
    end for

    ShowDetailsScreen(channelNode)
end sub
