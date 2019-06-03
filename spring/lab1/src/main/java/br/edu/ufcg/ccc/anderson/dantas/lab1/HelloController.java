package br.edu.ufcg.ccc.anderson.dantas.lab1;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.time.LocalTime;

@Controller
public class HelloController {

    @GetMapping("/hello")
    public String hello(@RequestParam(name="name", required = false, defaultValue = "World") String name,
            Model model) {
        model.addAttribute("name", name);
        String greeting = getGreeting();
        model.addAttribute("greeting", greeting);
        return "greeting";
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
