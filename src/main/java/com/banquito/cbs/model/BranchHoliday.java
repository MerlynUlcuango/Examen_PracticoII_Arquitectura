package com.banquito.cbs.model;

import lombok.Getter;
import lombok.Setter;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;

import java.time.LocalDate;
import java.util.Objects;

@Entity
@Table(name = "branch_holiday")
@Getter
@Setter
public class BranchHoliday {

    @Column(name = "date")
    private LocalDate date;

    @Column(name = "name")
    private String name;

    public BranchHoliday() {
    }

    public BranchHoliday(LocalDate date) {
        this.date = date;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof BranchHoliday)) return false;
        BranchHoliday that = (BranchHoliday) o;
        return Objects.equals(date, that.date);
    }

    @Override
    public int hashCode() {
        return Objects.hash(date);
    }

    @Override
    public String toString() {
        return "BranchHoliday{" +
                "date=" + date +
                ", name='" + name + '\'' +
                '}';
    }
}
