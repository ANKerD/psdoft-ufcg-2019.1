package br.edu.ufcg.anderson.dantas.lab1;

import org.springframework.web.bind.annotation.*;

@Controller
public class ApplicationController {

    @GetMapping("/hello")
    public String hello(){
        return "Hello world!";
    }
}
