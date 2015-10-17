REM Константы
LET R = 6371032;
LET GMP = 216;
LET target_angle = 81;

REM Параметры аппарата
LET M = 0.00001;
LET Mmax = 0.0026;
LET heater_on = FALSE;

REM Полетные параметры
LET horb = 650000;
LET w = -0.0614897;
LET M0 = -0.0018692;
LET t =  508.71901;

REM Углы начала/конца передачи
LET tr_start_angle = GMP - ACOS(R / (R + horb));
LET tr_stop_angle = GMP + ACOS(R / (R + horb));

LET dw = 0.01;
LET moment = FALSE;
LET da = 0.01;
LET sent = FALSE;

REM Начальная стаблизиция KA
WHEN cpu.flight_time == 0.0 DO
    CALL cpu.set_cycle(1);
    CALL orientation.start_torsion(M0);
END;

WHEN cpu.cycle == 1 AND cpu.flight_time >= t DO
    CALL cpu.set_cycle(3);
    CALL orientation.stop_torsion();
END;

WHEN cpu.cycle >= 2 DO
    IF moment == TRUE AND ABS(orientation.angular_velocity - w) < dw THEN
        CALL orientation.stop_torsion();
        moment = FALSE;
    ELSE
        IF orientation.angular_velocity > w THEN
            CALL orientation.start_torsion(0 - M);
            moment = TRUE;
        END;
        IF orientation.angular_velocity < w THEN
            CALL orientation.start_torsion(M);
            moment = TRUE;
        END;
    END;
END;

WHEN cpu.cycle == 3 AND navigation.angle + 1 > target_angle DO
	CALL load.set_mode("ON");
	CALL cpu.set_cycle(4);
END;

WHEN cpu.cycle == 4 AND navigation.angle - 1 > target_angle DO
	CALL radio.set_mode("ON");
	CALL telemetry.send_log_message("RADIO ON");
	CALL load.set_mode("OFF");
	CALL cpu.set_cycle(5);
END;

WHEN cpu.cycle == 5 DO
	IF ABS(navigation.angle - tr_start_angle) < da THEN
		CALL radio.set_mode("ON");
		CALL telemetry.send_log_message("TRANSMISSION STARTED");
	END;
	IF ABS(navigation.angle - tr_stop_angle) < da THEN
		CALL radio.set_mode("OFF");
		CALL telemetry.send_log_message("RADIO OFF");
		CALL telemetry.send_log_message("TRANSMISSION STOPPED");
	END;
END;


WHEN navigation.dark_side == TRUE AND heat_control.temperature < 283 DO
	CALL heat_control.start_heating();
	heater_on = TRUE;
END;

WHEN navigation.dark_side == FALSE AND heater_on == TRUE DO
	CALL heat_control.stop_heating();
	heater_on = FALSE;
END;

WHEN heat_control.temperature > 284 AND heater_on == TRUE DO
	CALL heat_control.stop_heating();
	heater_on = FALSE;
END;
