package com.example.demo.controller;

import com.example.demo.model.User;
import com.example.demo.repository.UserRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

@Controller
@RequestMapping("/users")
public class UserController {

    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // =========================
    // READ : Show all users
    // =========================
    @GetMapping
    public String listUsers(Model model) {
        model.addAttribute("users", userRepository.findAll());
        return "index";   // index.html
    }

    // =========================
    // CREATE : Add user
    // =========================
    @PostMapping
    public String addUser(@RequestParam String name) {
        User user = new User();
        user.setName(name);
        userRepository.save(user);
        return "redirect:/users";
    }

    // =========================
    // DELETE : Delete user
    // =========================
    @GetMapping("/delete/{id}")
    public String deleteUser(@PathVariable Long id) {
        userRepository.deleteById(id);
        return "redirect:/users";
    }

    // =========================
    // EDIT : Show edit page
    // =========================
    @GetMapping("/edit/{id}")
    public String editUser(@PathVariable Long id, Model model) {
        User user = userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid user id: " + id));

        model.addAttribute("user", user);
        return "edit-user";   // edit-user.html
    }

    // =========================
    // UPDATE : Save edited user
    // =========================
    @PostMapping("/update/{id}")
    public String updateUser(@PathVariable Long id,
                             @RequestParam String name) {

        User user = userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid user id: " + id));

        user.setName(name);
        userRepository.save(user);

        return "redirect:/users";
    }
}

