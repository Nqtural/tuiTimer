                      ###########################
                      ###   tuiTimer Config   ###
                      ###########################
 #####################################################################
#                                                                     #
#   Warning: All parameters must be set if this config file exists.   #
#                                                                     #
 #####################################################################

config = {
    "timer": {
        # Hide timer during solve
        "cover": False,
        
        # Amount of decimals to use when displaying timer throughout
        # the program. Does not affect how the times are stored
        # in the session. Range: 0 to 3
        "decimals": 4
    },
    "solves": {
        # Confirm before deleting solve
        "confirm-deletion": True
    },
    # Format: (forground, background)
    # Color values can be any 256-color
    "colors-ui": {
        # Default color
        "default": (7, 0),

        # Current tab color
        "tab-active": (1, 0),

        # Timer color when space is pressed but not long enough to
        # activate the timer
        "timer-primed": (1, 0),

        # Timer color when space is pressed long enough to activate
        # the timer
        "timer-ready": (2, 0),

        # Color of the selected solve in the solves tab
        "active-solve": (0, 6)
    },
    "colors-cube": {
        # Non-yellow stickers in the algorithms tab (only OLL view)
        "black": (244, 0),

        # Yellow (both OLL view and PLL view)
        "yellow": (226, 0),

        # Green (only PLL view)
        "green": (46, 0),

        # Blue (only PLL view)
        "blue": (21, 0),

        # Orange (only PLL view)
        "orange": (172, 0),

        # Red (only PLL view)
        "red": (196, 0)
    }
}
