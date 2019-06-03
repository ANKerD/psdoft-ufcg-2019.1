package br.edu.ufcg.ccc.anderson.dantas.lab1.rest;

import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalTime;

@RestController
public class GreetController {

    @GetMapping("/greeting")
    public Greeting greet(@RequestParam(name="name", required = false, defaultValue = "World") String name) {
        return new Greeting(name, getGreeting());
    }

    @GetMapping("/time")
    public ServerTime time(Model model) {
        LocalTime now = LocalTime.now();
        String currentTime = String.format("%02d:%02d:%02d", now.getHour(), now.getMinute(), now.getSecond());
        return new ServerTime(currentTime);
    }

    private String getGreeting() {
        LocalTime now = LocalTime.now();
        int hours = now.getHour();
        if (hours < 12)
            return "Bom dia";
        if (hours > 18)
            return "Boa noite";
        return "Boa tarde";
    }
}
