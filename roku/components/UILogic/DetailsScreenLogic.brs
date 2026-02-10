' DetailsScreenLogic.brs - Details screen handling
' Based on SceneGraph Master Sample pattern

sub ShowDetailsScreen(channelNode as Object)
    m.detailsScreen = CreateObject("roSGNode", "DetailsScreen")
    m.detailsScreen.content = channelNode
    m.detailsScreen.ObserveField("buttonSelected", "OnDetailsButtonSelected")
    m.selectedChannel = channelNode
    ShowScreen(m.detailsScreen)
end sub

sub OnDetailsButtonSelected()
    buttonIndex = m.detailsScreen.buttonSelected
    if buttonIndex = 0
        ' "Assistir agora" button
        ShowVideoScreen(m.selectedChannel)
    end if
end sub
