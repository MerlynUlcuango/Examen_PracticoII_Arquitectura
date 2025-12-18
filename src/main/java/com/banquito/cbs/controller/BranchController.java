package com.banquito.cbs.controller;

import com.banquito.cbs.dto.request.BranchCreateRequest;
import com.banquito.cbs.dto.request.BranchHolidayCreateRequest;
import com.banquito.cbs.dto.request.BranchUpdatePhoneRequest;
import com.banquito.cbs.model.Branch;
import com.banquito.cbs.model.BranchHoliday;
import com.banquito.cbs.service.BranchService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/v1/branches")
@Tag(name = "Branch API", description = "Gestión de sucursales y feriados")
public class BranchController {

    private final BranchService branchService;

    public BranchController(BranchService branchService) {
        this.branchService = branchService;
    }

    @Operation(summary = "Obtener todas las sucursales")
    @GetMapping
    public ResponseEntity<List<Branch>> getAllBranches() {
        log.info("CONTROLLER - Obtener todas las sucursales");
        return ResponseEntity.ok(branchService.getAllBranches());
    }

    @Operation(summary = "Crear una nueva sucursal")
    @PostMapping
    public ResponseEntity<Branch> createBranch(
            @Valid @RequestBody BranchCreateRequest request) {

        log.info("CONTROLLER - Crear sucursal id={}", request.getId());
        Branch branch = branchService.createBranch(request);
        return new ResponseEntity<>(branch, HttpStatus.CREATED);
    }

    @Operation(summary = "Obtener sucursal por ID")
    @GetMapping("/{id}")
    public ResponseEntity<Branch> getBranchById(@PathVariable Integer id) {
        log.info("CONTROLLER - Obtener sucursal por id={}", id);
        Branch branch = branchService.getBranchById(id);
        return ResponseEntity.ok(branch);
    }

    @Operation(summary = "Actualizar número de teléfono de una sucursal")
    @PatchMapping("/{id}/phone")
    public ResponseEntity<Branch> updateBranchPhone(
            @PathVariable Integer id,
            @Valid @RequestBody BranchUpdatePhoneRequest request) {

        log.info("CONTROLLER - Actualizar teléfono sucursal id={}", id);
        Branch branch = branchService.updateBranchPhone(id, request);
        return ResponseEntity.ok(branch);
    }

    @Operation(summary = "Agregar un feriado a una sucursal")
    @PostMapping("/{id}/holidays")
    public ResponseEntity<Branch> addHoliday(
            @PathVariable Integer id,
            @Valid @RequestBody BranchHolidayCreateRequest request) {

        log.info("CONTROLLER - Agregar feriado sucursal id={} date={}", id, request.getDate());
        Branch branch = branchService.addHoliday(id, request);
        return ResponseEntity.ok(branch);
    }

    @Operation(summary = "Eliminar un feriado de una sucursal")
    @DeleteMapping("/{id}/holidays/{date}")
    public ResponseEntity<Branch> removeHoliday(
            @PathVariable Integer id,
            @PathVariable LocalDate date) {

        log.info("CONTROLLER - Eliminar feriado sucursal id={} date={}", id, date);
        Branch branch = branchService.removeHoliday(id, date);
        return ResponseEntity.ok(branch);
    }

    @Operation(summary = "Obtener todos los feriados de una sucursal")
    @GetMapping("/{id}/holidays")
    public ResponseEntity<List<BranchHoliday>> getHolidays(@PathVariable Integer id) {
        log.info("CONTROLLER - Obtener feriados sucursal id={}", id);
        return ResponseEntity.ok(branchService.getHolidays(id));
    }

    @Operation(summary = "Verificar si una fecha es feriado en una sucursal")
    @GetMapping("/{id}/holidays/{date}/exists")
    public ResponseEntity<Boolean> isHoliday(
            @PathVariable Integer id,
            @PathVariable LocalDate date) {

        log.info("CONTROLLER - Verificar feriado sucursal id={} date={}", id, date);
        boolean result = branchService.isHoliday(id, date);
        return ResponseEntity.ok(result);
    }
}
