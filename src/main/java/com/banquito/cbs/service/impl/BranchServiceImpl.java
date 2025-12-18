package com.banquito.cbs.service.impl;

import com.banquito.cbs.dto.request.BranchCreateRequest;
import com.banquito.cbs.dto.request.BranchHolidayCreateRequest;
import com.banquito.cbs.dto.request.BranchUpdatePhoneRequest;
import com.banquito.cbs.model.Branch;
import com.banquito.cbs.model.BranchHoliday;
import com.banquito.cbs.repository.BranchRepository;
import com.banquito.cbs.service.BranchService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Slf4j
@Service
public class BranchServiceImpl implements BranchService {

    private final BranchRepository repository;

    public BranchServiceImpl(BranchRepository repository) {
        this.repository = repository;
    }

    @Override
    public List<Branch> getAllBranches() {
        log.info("SERVICE - Obtener todas las sucursales");
        return repository.findAll();
    }

    @Override
    public Branch createBranch(BranchCreateRequest request) {
        log.info("SERVICE - Crear sucursal");

        Branch branch = new Branch();
        branch.setId((int) (System.currentTimeMillis() % 100000));
        branch.setEmailAddress(request.getEmailAddress());
        branch.setName(request.getName());
        branch.setPhoneNumber(request.getPhoneNumber());
        branch.setState("ACTIVE");
        branch.setCreationDate(LocalDateTime.now());
        branch.setLastModifiedDate(LocalDateTime.now());
        branch.setBranchHolidays(new ArrayList<>());

        return repository.save(branch);
    }

    @Override
    public Branch getBranchById(Integer id) {
        log.info("SERVICE - Buscar sucursal por id={}", id);
        return repository.findById(id)
                .orElseThrow(() -> new RuntimeException("Sucursal no encontrada con id=" + id));
    }

    @Override
    public Branch updateBranchPhone(Integer id, BranchUpdatePhoneRequest request) {
        Branch branch = getBranchById(id);
        branch.setPhoneNumber(request.getPhoneNumber());
        branch.setLastModifiedDate(LocalDateTime.now());
        return repository.save(branch);
    }

    @Override
    public Branch addHoliday(Integer id, BranchHolidayCreateRequest request) {
        Branch branch = getBranchById(id);

        if (branch.getBranchHolidays() == null) {
            branch.setBranchHolidays(new ArrayList<>());
        }

        BranchHoliday holiday = new BranchHoliday();
        holiday.setDate(request.getDate());
        holiday.setName(request.getName());

        branch.getBranchHolidays().add(holiday);
        branch.setLastModifiedDate(LocalDateTime.now());

        return repository.save(branch);
    }

    @Override
    public Branch removeHoliday(Integer id, LocalDate date) {
        Branch branch = getBranchById(id);
        branch.getBranchHolidays().removeIf(h -> h.getDate().equals(date));
        branch.setLastModifiedDate(LocalDateTime.now());
        return repository.save(branch);
    }

    @Override
    public List<BranchHoliday> getHolidays(Integer id) {
        return getBranchById(id).getBranchHolidays();
    }

    @Override
    public boolean isHoliday(Integer id, LocalDate date) {
        return getBranchById(id).getBranchHolidays()
                .stream()
                .anyMatch(h -> h.getDate().equals(date));
    }
}
