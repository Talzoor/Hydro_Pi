def main():
    global NEED_TO_CLOSE, MICRO_S_CHANGE, WATER_LEVEL_SWITCH
    try:
        LOG.debug("Flow_pin:{}".format(FLOW_PIN))
        time_start = int(round(time.time()))
        debug_print = True

        while True:
            time_now = int(round(time.time()))
            # check to see if there is water flow
            flowing = check_flow(2)
            if debug_print: LOG.debug("flowing:{}".format(flowing))

            if WATER_LEVEL_SWITCH:
                #open tap (tap)
                pass

                if time_check and not flowing:
                    #change (tap)
                    pass
            else:
                #close (taps)
                pass

            if (tap is not 0) and (not flowing):
                somthing_bad+=1


            if WATER_LEVEL_SWITCH:
                MICRO_S_CHANGE = False
                if SOLENOID_OPEN == 0:
                    open_solenoid(1)                # open tap_1
                    # LOG.info("opening tap 1")
                if not flowing:
                    if NEED_TO_CLOSE:
                        open_solenoid(0)
                    else:
                        if SOLENOID_OPEN == 1:
                            open_solenoid(2)            # open tap_2
                        if not flowing:
                            something_wrong("NO WATER")
                            open_solenoid(0)
                            # error! send email no water
            else:                                    # water_level == False (micro off)

                if NEED_TO_CLOSE:
                    open_solenoid(0)
                    while flowing:
                        LOG.info("closing taps")
                        open_solenoid(0)
                        NEED_TO_CLOSE += 1
                        if NEED_TO_CLOSE > 5:
                            something_wrong("DRIPPING")
                            # error! send email DRIPPING
                        LOG.debug("flowing:{}".format(flowing))
                        if MICRO_S_CHANGE:
                            MICRO_S_CHANGE = False
                            break
                    NEED_TO_CLOSE = 0
                else:
                    if flowing:
                        open_solenoid(0)
                        # NEED_TO_CLOSE += 1
                        # if NEED_TO_CLOSE > 5:
                        #     something_wrong()
                            # error! send email DRIPPING
                    else:
                        if debug_print: LOG.debug("all good, all closed")

            sleep(CHECK_EVERY)

            debug_print = False

            if time_now - time_start > DEBUG_PRINT_EVERY:
                time_start = time_now
                debug_print = True


    except KeyboardInterrupt:
        LOG.info("Keyboard Exc.")
        raise KeyboardInterrupt
    except:
        raise_exception("main")

    finally:
        close()